from collections import defaultdict
import regex as re
import neo4j
from CyVer.utils import *
import pandas as pd

class SyntaxValidator:
    """
    A class to validate Cypher queries for correct syntax and label consistency.
    """

    def __init__(self, driver , check_multilabeled_nodes=True):
        """
        Initialize the validator with a Neo4j driver.

        Args:
            driver: An instance of the Neo4j driver.
            check_multilabeled_nodes (bool): Whether to check for multilabeled nodes (default: True).

        Raises:
            TypeError: If the driver is not a valid Neo4j driver.
        """
        # Check if driver is an instance of the Neo4j GraphDatabase driver
        if not isinstance(driver, neo4j.Driver):
            raise TypeError("Provided driver is not a valid Neo4j driver (instance of neo4j.Driver).")
        
        self.driver = driver

        # Multilabel nodes
        self.check_multilabeled_nodes = check_multilabeled_nodes
        self.multilabels =  None 

        if  self.check_multilabeled_nodes:
            """Fetch and store multilabeled nodes"""
            rel_query = "MATCH (n) WHERE size(labels(n)) > 1 WITH DISTINCT labels(n) AS labelList RETURN COLLECT(labelList) AS output"
            self.multilabels = self.__read_cypher_query(rel_query)

    def __read_cypher_query(self, query=None, params=None):
        """
        Executes a Cypher query using the instance's driver and query.

        Args:
            query (str, optional): The Cypher query to execute. If not provided, it uses the instance's `query`.
            params (dict, optional): Query parameters. Defaults to None.

        Returns:
            dict: The result of the query execution (assumes a single output).
        """
        with self.driver.session() as session:
            result = session.run(query, parameters=params if params else {})
            return result.single()['output']

    def validate(self,query, database_name=None):
        """
        Check if the query has correct Cypher syntax.

        Args:
            query (str): The Cypher query to validate.
            database_name (str | None) :Database to validate the query against. None (default) uses the database configured on the server side.

        Returns:
            bool: True if the syntax is correct, False otherwise.

        Prints a message if there are variables with conflicting labels.
        """
        
        # Modify the query to use EXPLAIN for checking the execution plan, whithout executing it 
        explain_query = f"EXPLAIN {query}"

        try:
            records, summary, keys = self.driver.execute_query(explain_query, database_= database_name) #notifications_min_severity='OFF'
            
            # Detect specific types of warnings in the query
            if summary.notifications:
                for notification in summary.notifications:
                    if notification['code'] in['Neo.ClientNotification.Statement.ParameterNotProvided', 
                                            'Neo.ClientNotification.Statement.UnsatisfiableRelationshipTypeExpression']: 
                        return False
                    
            # Detect arithmetic errors of explicit division by zero that will result 
            # in Neo.ClientError.Statement.ArithmeticError in execution
            # but not arithmetic errors that may occur due to a divisor becoming zero at execution time
            # Regex pattern to catch explicit " / 0", " / 0.0", or " / (0)"
            divisor_zero_pattern = r'/\s*(?:\(\s*0(?:\.0*)?\s*\)|0(?:\.0*)?)\s*(?![\w(])'
            if re.search(divisor_zero_pattern, query):
                return False
            
            #----------To detect conflicting labels----------------
            
            # Find nodes or rels with label (even if they are followed by property access in {})
            matches = re.findall(r"[\(\[](\s*\w+\s*):(\s*\w+\s*)(?:\s*\{[^\}]*\})?[\)\]]", query)
                                
            # Dictionary to store variables and their associated labels
            variable_labels = defaultdict(set)  # initializes each key with an empty set
    
            # Populate the dictionary with variables and corresponding labels
            for var, label in matches:
                variable_labels[var.strip()].add(label.strip())
            # Find conflicting variables
            # Conflicting variables are considered if they have the same variable name but different labels 
            # and the labels are not part of the multilabels (if multilabels check is True)
            if self.check_multilabeled_nodes:
                # When checking for multilabeled nodes, only consider conflicting variables that are not part of multilabels
                conflicting_vars = {
                    var: labels
                    for var, labels in variable_labels.items()
                    if len(labels) > 1 and not self.__subset_in_multilabels(labels, self.multilabels)
                }
            else:
                # If not checking multilabeled nodes, just consider conflicting variables that have multiple labels
                conflicting_vars = {
                    var: labels
                    for var, labels in variable_labels.items()
                    if len(labels) > 1
                }

            # If conflicting variables exist, raise an error
            if conflicting_vars:
                for var, labels in conflicting_vars.items():
                    print(f"Variable '{var}' has conflicting labels: {', '.join(labels)}")
                return False
            return True
        except Exception as e:
            # Detects:
            # -Neo.DatabaseError.Statement.ExecutionFailed
            # -Neo.ClientError.Statement.SyntaxError
            # print('The error is ' , e.code)
            return False

    # This method does not require access to any instance or class data. It is  purely a utility function that performs an operation (addition) and 
    # returns the result. Static methods are typically used when the method does not need to modify or access the object's state.
    @staticmethod
    def __subset_in_multilabels(subset, list_of_lists):
        """
        Check if a subset exists within a list of lists.

        Args:
            subset (list): The subset to search for.
            list_of_lists (list): A list of lists to search within.

        Returns:
            bool: True if the subset is found in any inner list, False otherwise.
        """
        for inner_list in list_of_lists:
            # Check if `subset` is a subset of `inner_list`
            if all(item in inner_list for item in subset):
                return True
        return False
    
class SchemaValidator:
    """
    A class to validate Cypher queries against a predefined schema.

    This class ensures that Cypher queries conform to the structural constraints defined in a database schema. 
    It validates whether the nodes, relationships, and paths referenced in a query
    align with the expected schema structure, helping to maintain consistency
    and prevent errors.
    """

    def __init__(self, driver):
        """
        Initialize the validator with a Neo4j driver.

        Args:
            driver: An instance of the Neo4j driver.

        Raises:
            TypeError: If the driver is not a valid Neo4j driver.
        """
        # Check if driver is an instance of the Neo4j GraphDatabase driver
        if not isinstance(driver, neo4j.Driver):
            raise TypeError("Provided driver is not a valid Neo4j driver (instance of neo4j.Driver).")
        
        self.driver = driver


    def __check_path_exists(self, pattern, database_name=None):
        """
        Check if the provided pattern exist in the Neo4j Database

        Args:
            pattern: cypher pattern
            database_name (str | None) :Database to validate the query against. None (default) uses the database configured on the server

        Returns:
            bool: True if the pattern exists , False otherwise.
        """
        statement = f'''
        MATCH p = {pattern} 
        RETURN COUNT(p) > 0 AS path_exists
        '''
        try:
            # Execute the query with notifications off
            records, _, _ = self.driver.execute_query(statement, notifications_min_severity='OFF',  database_=database_name,)

            # Access the 'path_exists' field from the result
            return bool(records[0]['path_exists'])

        except Exception as e:
            # Check for syntax error specifically, or other exceptions
            if hasattr(e, 'code') and e.code != 'Neo.ClientError.Statement.SyntaxError':
                print(f"Some other type of Neo4jError of {statement} : {e.code}")
                # print(e.code)
                # print(pattern)
            return False

    def extract(self,query, database_name=None):
        """
        Extract the nodes, relationships and paths of the provided query

        Args:
            query (str): The Cypher query to validate.
            database_name (str | None) :Database to validate the query against. None (default) uses the database configured on the server side.

        Returns:
            Three lists containing the nodes, the relationships and the paths in the cypher query
        """
        # Replace -- with empty relationship
        query = query.replace("--", "-[]-")

        # pattern of nodes
        node_pattern = r"\(\s*(\s*\w+\s*:\s*\w+\s*|\s*\w*\s*|:\s*\w+\s*|)\s*(\{[^}]*\})?\s*\)"
        # pattern of relationships
        rel_pattern = r"\[\s*(\s*\w+\s*:\s*\w+\s*|\s*\w*\s*|:\s*\w+\s*|)\s*(\{[^}]*\})?\s*\]"
        # combine node and relationships patterns
        path_pattern= rf'({node_pattern}\s*<?-\s*{rel_pattern}\s*->?\s*{node_pattern})'

        # Extract paths
        matches = re.findall(path_pattern,query,overlapped=True)

        # specify only node if no detected relationships without ? after :, only nodes with labels
        nodes_with_label = r"\(\s*(\s*\w*\s*:\s*\w+\s*)\s*(\{[^}]*\})?\s*\)"
        # specify only node if no detected relationships without * after :, only nodes with labels
        rels_with_label =  r"\[\s*(\s*\w*\s*:\s*\w+\s*)\s*(\{[^}]*\})?\s*\]"

        # Extract labeled nodes and relationships using regex
        nodes_matches = re.findall(nodes_with_label, query)
        rels_matches = re.findall(rels_with_label, query)

        # Dict of key the variables in query and value the label of the rel or node
        nodes_dict = {key.strip() or f"_empty_{i}": value.strip() for i, (key, value) in enumerate(match[0].split(":", 1) for match in nodes_matches)}
        rels_dict = {key.strip() or f"_empty_{i}": value.strip() for i, (key, value) in enumerate(match[0].split(":", 1) for match in rels_matches)}
        elements_dict = {**nodes_dict, **rels_dict}

        # The nodes labels
        node_labels = list(set(nodes_dict.values()))
        node_paths = ['(:' + node_label + ')' for node_label in node_labels]

        # The rels labels
        rel_labels = list(set(rels_dict.values()))
        rel_paths = ['()-[:' + rel_label + ']-()' for rel_label in rel_labels]

        # If we have at least one path in the cypher query
        if matches:
            # Add counter for unknown params
            counter = 1
            # A set containing the paths for inference
            inference_paths,paths = set(),set()

            # Stage 1: Replace identifiers in already mentioned in the cypher query
            for match in matches:

                # Step 1: Delete extra spaces
                path = re.sub(r'\s+','',match[0])

                # Step 2: Delete {} properties inside nodes and rels
                match_wt_prop = re.sub(r"\{[^}]*\}", "", path)
                
                # Step 3: Add labels to variables if specified in another match clause
                path_with_node_rels_labels = replace_with_labels(match_wt_prop, elements_dict) # replace i to i:Indicator

                # Step 4: Loop through each occurrence of () or [] and replace them with a variable name
                while "()" in path_with_node_rels_labels or "[]" in path_with_node_rels_labels:
                    path_with_node_rels_labels = path_with_node_rels_labels.replace("()", f"(unknown_variable_{counter})", 1) if "()" in path_with_node_rels_labels else path_with_node_rels_labels.replace("[]", f"[unknown_variable_{counter}]", 1)
                    counter += 1

                # Step 5: Inference - Find variables in relationships or nodes
                if any(filter(None, re.findall(r"\((\w+)\)|\[(\w+)\]", path_with_node_rels_labels))):
                    # add to inference paths
                    inference_paths.add(self.__remove_prefix_before_colon(path_with_node_rels_labels))

                # Step 6: Add to paths
                paths.add(self.__remove_prefix_before_colon(path_with_node_rels_labels))

                # Step 7: Isolate not inference paths
                not_inference_paths = paths - inference_paths

            # print('Paths before inference:', inference_paths)
            
            # Stage 2: Combine them with the provided schema
            # If exist inference paths
            if inference_paths:
                # Copy not inference paths to combine them
                paths_after_inference = not_inference_paths.copy()
                # Create a dict with key the unknown variable and value a random variable from the df if is not empty else ""
                inference_dict={}
                for df in get_paths_after_inference(self.driver,list(inference_paths),database_name):
                    if df.empty:
                        for col in df.columns:
                            inference_dict[col]=""
                    else:
                        df1_inf = df.sample(1).reset_index(drop=True)
                        for col in df.columns:
                            inference_dict[col] = df1_inf.iloc[0][col]
                # Loop over the inference paths to replace with labels
                for inference_match in inference_paths:
                    # First we replace the nodes or the rels with the inferred labels
                    # Second we remove prefix for patterns n:Label1
                    paths_after_inference.add(self.__remove_prefix_before_colon(replace_with_labels(inference_match,inference_dict)))

                return node_paths,rel_paths,list(paths_after_inference)
            return node_paths,rel_paths,list(paths)
        else:
            return node_paths,[],[]
        
    def validate(self,query, database_name=None):
        """
        Validate the correctness of  the nodes, relationships and paths of the provided query

        Args:
            query (str): The Cypher query to validate.
            database_name(str | None): The name of the database to validate the query against. None (default) uses the database configured on the server side.

        Returns:
            A score in [0,1] : a weighted average of the correct nodes,relationships and paths with equal weights
        """

        nodes,rels,paths = self.extract(query, database_name)
        
        if paths:
            if nodes:
                if rels:
                    common_nodes = sum(self.__check_path_exists(node,database_name) for node in nodes)
                    common_rels = sum(self.__check_path_exists( rel, database_name) for rel in rels)
                    common_paths = sum(self.__check_path_exists( path, database_name) for path in paths)
                    # print(common_paths,common_nodes,common_rels)
                    score = 1/3 * ((common_rels) / len(rels)) + 1/3 * ((common_nodes) / len(nodes)) + 1/3 * ((common_paths) / len(paths))

                else:
                    common_nodes = sum(self.__check_path_exists( node, database_name) for node in nodes)
                    common_paths = sum(self.__check_path_exists( path, database_name) for path in paths)

                    score = 0.5 * ((common_nodes) / len(nodes)) +  0.5 * ((common_paths) / len(paths))

            else:
                if rels:
                    common_rels = sum(self.__check_path_exists( rel, database_name) for rel in rels)
                    common_paths = sum(self.__check_path_exists( path, database_name) for path in paths)

                    score = 0.5 * ((common_rels) / len(rels)) + 0.5 * ((common_paths) / len(paths))
                else:
                    common_paths = sum(self.__check_path_exists( path, database_name) for path in paths)
                    score = ((common_paths) / len(paths))
                    # raise ValueError("Both 'rels' and 'nodes' lists are empty while existing paths")
        else:
            if nodes:
                common_nodes = sum(self.__check_path_exists( node, database_name) for node in nodes)
                score = ((common_nodes) / len(nodes))
            else:
                score = 1

        return score

    # This method does not require access to any instance or class data. It is  purely a utility function that performs an operation (addition) and 
    # returns the result. Static methods are typically used when the method does not need to modify or access the object's state.
    @staticmethod
    def __remove_prefix_before_colon(txt):
        """
        Remove prefix before colon

        Args:
            txt (str): a:example

        Returns:
            :example
        """
    # Regex to remove anything before the colon in both nodes and relationships
        return re.sub(r'\b\w+:(\w*)', r':\1', txt)

class PropertiesValidator:
    """
    A class to validate the correctness of property access in Cypher queries against a predefined schema.

    This class ensures that Cypher queries access only valid properties for nodes
    and relationships based on their labels or types.
    """

    def __init__(self, driver):
        """
        Initialize the validator with a Neo4j driver.

        Args:
            driver: An instance of the Neo4j driver.

        Raises:
            TypeError: If the driver is not a valid Neo4j driver.
        """
        # Check if driver is an instance of the Neo4j GraphDatabase driver
        if not isinstance(driver, neo4j.Driver):
            raise TypeError("Provided driver is not a valid Neo4j driver (instance of neo4j.Driver).")
        
        self.driver = driver

    def __check_label_type(self, label, database_name=None):
        """
        Check if a given label is a node label or a relationship type.
        Args:
            - label(string): The label to check.
            - database_name (str | None) :Database to validate the query against. None (default) uses the database configured on the server side.
        Returns:
            string: "node" or "relationship", "none" otherwise.
        """
        # Query for node labels
        node_query = f"""
        CALL db.labels()
        YIELD label
        WHERE label = '{label}'
        RETURN COUNT(label) > 0 AS is_node_label
        """
        
        # Query for relationship types
        rel_query = f"""
        CALL db.relationshipTypes()
        YIELD relationshipType
        WHERE relationshipType = '{label}'
        RETURN COUNT(relationshipType) > 0 AS is_relationship_type
        """
        
        # Execute both queries
        node_result = self.driver.execute_query(node_query, database_= database_name)
        rel_result = self.driver.execute_query(rel_query, database_= database_name)
        
        # Determine the type
        is_node_label = node_result[0][0]['is_node_label'] if node_result else False
        is_relationship_type = rel_result[0][0]['is_relationship_type'] if rel_result else False
        
        # Return the result
        if is_node_label:
            return "node"
        elif is_relationship_type:
            return "relationship"
        else:
            return "none"
        
    def __query_prop_exist(self, label, property, database_name = None):
        '''Check if this property exists for the defined label
        Args:
            - label(str): The label to check.
            - property (str): The property to check.
            - database_name (str | None) :Database to validate the query against. None (default) uses the database configured on the server side.
            
        Returns:
            - bool: True if the property exists , False otherwise.
        '''
        property_exists = False
        type = self.__check_label_type(label, database_name)
        if type != 'none': # the label does not exist in the graph
            if type=='node':
                check_cypher = f"MATCH (x:{label}) WHERE (x.{property}) IS NOT NULL RETURN COUNT(x) > 0 AS exists"
            elif type=='relationship':
                check_cypher = f"MATCH ()-[x:{label}]-() WHERE (x.{property}) IS NOT NULL RETURN COUNT(x) > 0 AS exists "
            records = self.driver.execute_query(check_cypher,database_=database_name)
            property_exists = records[0][0]['exists']
        
        return property_exists
    
    def __get_inferred_labels_properties (self,strict, var_label_map,label_props_map, var_props_map, query, database_name=None):
        '''
        Infers labels for variables that are missing labels but access properties and updates the label_props_map dict(that 
        maps the labels with the properties they access) with the inferred labels for variables that lacked them and their accessed properties .

        Args:
        - strict (bool): Determines the behavior of the function when trying to match labels:
            - If True, the function will only return the first valid label-property pair that correctly matches all properties.
            - If False, the function will return the label-property pair that matches the most properties correctly, even if some properties remain unmatched.
        - var_label_map (dict): A mapping of variables to their corresponding labels.
        - label_props_map (dict): A mapping of labels to the properties they access.
        - var_props_map (dict): A mapping of variables to the properties they access.
        - query (object): The query used for inference, which may be utilized to gather further data.
        - database_name (str | None): The name of the database to validate the query against. None (default) uses the database configured on the server side.

        Returns:
        - dict: A dictionary containing the inferred label-property mappings, where the labels are the inferred ones for unknown variables.
        '''
        # Infer the unknown variables
        inference_paths = self.__prepare_query_for_infer (var_label_map, query)
        df_valid_label_pairs = get_paths_after_inference (self.driver,inference_paths, database_name) #list of df with inferred labels of vars 
        for df_var_labels in df_valid_label_pairs:
            #keep the columns that refer to variables that access properties
            cols_to_keep = [col for col in df_var_labels.columns if col in var_props_map]
            if cols_to_keep:
                df_filtered = df_var_labels[cols_to_keep].drop_duplicates()
            else:
                df_filtered = pd.DataFrame()  
            
            #If the df has one row (then the variable has to be a specific label)
            if len(df_filtered.index) == 1:
                #---ALWAYS STRICT=FALSE APPROACH-----
                # for var in  df_filtered.columns:
                #     label = df_filtered[var].iloc[0]
                #     #add to the label_props_map the properties accessed by this label (infereed by the var)
                #     label_props_map = self.__extend_dict_with_list_elements (label_props_map, label, var_props_map[var])
                #--------------------------------------

                valid_label = True #All the labels have all their properties valid
                label_props = {} #Each inferred label which properties accesses based on the var(var_props_map)
                for variable in  df_filtered.columns:
                    label = df_filtered[variable].iloc[0] # map the variable to the label
                    #the label accesses these properties
                    label_props = self.__extend_dict_with_list_elements (label_props, label, var_props_map[variable])
                    for accessed_prop in var_props_map[variable]:
                        #check if ALL the properties accessed by this label are valid
                        if not self.__query_prop_exist(label, accessed_prop, database_name):
                            valid_label = False #at least one property of one label of the label pairs is not valid
                if valid_label:
                    # print('The label has all its properties valid')
                    #add to the label_props_map the properties accessed by this label (inferred by the var)
                    label_props_map = self.__extend_dict_with_list_elements (label_props_map, label, label_props[label])
                else:
                    #if strict: i dont care about these properties
                    if not strict:
                        #i return the label 
                        label_props_map = self.__extend_dict_with_list_elements (label_props_map, label, label_props[label])
            elif len(df_filtered.index) > 1: #if it has multiple pairs of valid labels
                #  we need to find at least one pair for which all the accessed properties are valid
                # if none pair is found we return the pair that offers the max accessed properties  
                label_pair_correct_props = {} #map each label pair(row of df) with total number of correct props accessed     
                for index, row in df_filtered.iterrows():
                    total_correct_props = 0 #counter per row (label pairs) with correct properties, used when a valid label pair for all properties was not found)
                    #For dependend variables (columns of the dataframe) the properties accessed have to be valid for all labels
                    valid_label = True #All the labels have all their properties valid
                    label_props = {} #Each inferred label which properties accesses based on the var(var_props_map)
                    for variable in  df_filtered.columns:
                        label = row[variable] # map the variable to the possible label
                        #the label accesses these properties
                        label_props = self.__extend_dict_with_list_elements (label_props, label, var_props_map[variable])
                        for accessed_prop in var_props_map[variable]:
                            #check if ALL the properties accessed by this label are valid
                            if not self.__query_prop_exist(label, accessed_prop, database_name):
                                valid_label = False #at least one property of one label of the label pairs is not valid
                            else:
                                total_correct_props+=1 
                    label_pair_correct_props[index] = total_correct_props  
                    if valid_label:
                        # print('All the labels have all  their properties valid')
                        
                        #add the valid pair of labels and their properties
                        for label in label_props:
                            label_props_map = self.__extend_dict_with_list_elements (label_props_map, label, label_props[label])
                        break #stop searching the label pairs
                if not valid_label:
                    #if strict: i dont care about these properties                    
                    if not strict :
                        #i get the label pair that accesses the max correct properties
                        
                        max_index = max(label_pair_correct_props, key=label_pair_correct_props.get)
                        label_props = {}
                    
                        for variable in  df_filtered.columns:
                            label = df_filtered.loc[max_index, variable]
                            #the label accesses these properties
                            label_props = self.__extend_dict_with_list_elements (label_props, label, var_props_map[variable])
                        
                        for label in label_props:
                            label_props_map = self.__extend_dict_with_list_elements (label_props_map, label, label_props[label])
                                
        return label_props_map
    
    def extract(self,query,database_name = None, strict=False):
        """
        Extract the properties accessed by each label of the provided query

        Args:
            query (str): The Cypher query to validate.
            strict (bool): Determines the behavior of the function when trying to infer labels:

        Returns:
            Mappings of:
                var_props_map: variables with properties they access
                label_props_map: labels (inferred and not) with the properties they access
        """
        #Get the properties accessed by each label (label_props_map)
        var_label_map, label_props_map, var_props_map = self.__get_var_labels_props (query)
        
        # If there are variables with no matched labels that access properties, we need to infer their labels
        if var_props_map:
            label_props_map = self.__get_inferred_labels_properties (strict, var_label_map,label_props_map, var_props_map, query, database_name)
        
        return var_props_map,label_props_map
    
    def validate(self,query,database_name = None, strict=False):
        """ 
        Validate the correctness of the properties accessed by labels  in the given query against the provided schema.

        Args:
            query (str): The Cypher query to validate.
            database_name (str | None): The name of the database to validate the query against. None (default) uses the database configured on the server side.
            strict (bool): Determines the behavior of the function when trying to infer labels:

        Returns:
            Precission score in [0,1] : of the correct_props / total_props
            None if there were no properties accessed
        """
        _, label_props_map = self.extract(query,database_name, strict)
        if label_props_map:
            #How many of the total properties accessed are valid according to their label)
            correct_props = sum(
                self.__query_prop_exist(label, property, database_name)
                for label, properties in label_props_map.items()
                for property in properties
            )
            total_props = sum(len(properties) for properties in label_props_map.values())

            # Calculate precision
            precision = correct_props / total_props #if total_props > 0 else 1
        
            return precision
        
        return None #if no property was accessed

    @staticmethod
    def __extend_dict_with_list_elements (mydict, key, list_value):
        ''' 
        Add to mydict a new key if it doesnt exist with value the given list
        If the key exists extend the value list with no duplicate elements of the given list
        Args:
        - mydict (dict): The dictionary to modify.
        - key (hashable): The key to check or add.
        - list_value (list): The list of elements to add or extend.

        Returns:
        - mydict: The modified dictionary .
        '''
        if key not in mydict:
            mydict[key] = list_value
        else: 
            mydict[key].extend(
                prop for prop in list_value if prop not in mydict[key]
            )
        return mydict
    
    @staticmethod
    def __inline_var_label_properties_mapping ( query ):
        """ 
        Extracts from the query the mapping of nodes and relationship labels with their properties
        (properties accessed inside) and the mapping of variables and labels.
        
        The pattern matched: matches = [('var:Label','{ property_name : property_value}'), ...]
        
        Args:
            query (str): The Cypher query to validate.
        Returns:
            Dict (labels_props_map) that maps the label (of a node or a relationship ) with a list of its properties 
            accessed in the query 
            Dict (var_label_map) that maps any variables with their labels 
        """

        label_props_map = {} #Map each label with the properties mentioned
        var_label_map = {} #Map each var with the label mentioned (in case the variable is mentioned again without its label)

        #Find patterns of nodes or relationships that define their label
        # To match a node: optional_variable:label{optional properties} 
        node_pattern = r"\(\s*(\w*\s*:\s*\w+)\s*(\{[^}]*\})?\s*\)"
        # To match a relationship: optional_variable:label{optional properties} 
        rel_pattern = r"\[\s*(\w*\s*:\s*\w+)\s*(\{[^}]*\})?\s*\]"
        # Match nodes and relationships separately
        node_matches = re.findall(node_pattern, query)
        rel_matches = re.findall(rel_pattern, query)
        matches = [ match for match in node_matches] + [ match for match in rel_matches]
        # matches = [('var:Label','{ property_name : property_value}'), ...]

        #-------------------------------------------------------------------------------------
        #---------For properties accessed inside the node or relationship --------------------
        #-------------------------------------------------------------------------------------
        label_pattern = r":(.*)" #extract the label name
        var_pattern = r"(.*):" #extract the var
        property_pattern = r"\b(\w+)\s*:" #extract the property name (up to :) from the properties accessed inside 

        
        for match in matches:
            #Extract the label
            label = re.search(label_pattern, match[0]).group(1).strip()

            #Extract the var if any
            var = re.search(var_pattern, match[0]).group(1).strip()
            if var: 
                var_label_map[var] = label
                    
            #Extract the properties
            properties = set () # To avoid duplicates 
            if match[1] :# this node or rel with label has also poperties inside
                # Remove from the properties anything included in single quotes ' ' which will be any values (we will avoid : in values that appear in datetimes)
                remove_pattern = r"'[^']*'"
                cleared_match = re.sub(remove_pattern, '', match[1])
                properties.update(re.findall(property_pattern,cleared_match ))
                properties = list(properties)
                label_props_map = PropertiesValidator.__extend_dict_with_list_elements (label_props_map, label, properties)
        return var_label_map, label_props_map
    
    @staticmethod
    def __outside_var_properties_mapping (var_label_map,label_props_map, query):
        ''' 
        Checks in the query if the variables that are mapped with a label (in var_label_map dict) access properties
        outside (in where, return, etc) in format var.property. If they do we update the properties accessed by the
        corresponding label in label_props_map. 
        If we find a variable that accesses a property but we dont have a matching label, we keep this mapping in vars_prop_dict
        (the label of this variable will be inferred)
        Args:
            Dict (var_label_map) that maps any variables with their labels 
            Dict (label_props_map), that maps labels with properties they access
            query (str): The Cypher query to validate.
        Returns:
            Dict (var_label_map) that maps variables with their labels 
            Dict (label_props_map), that maps labels with properties they access,  updated. 
        '''
        var_props_map = {} # The dict that maps variables wih accessed properties
        
        #Find all vars that access a property - Ensure the var pattern is found outside single ('') or double ("") quotes so it is not a value
        # var_property_pattern = r"(?<!')\b(\w+)\s*\.\s*(\w+)\b(?!')" #single quotes only
        var_property_pattern = r'(?<!["\'])\b(\w+)\s*\.\s*(\w+)\b(?!["\'])'

        
        var_props = re.findall(var_property_pattern,query) #each variable matched with its property
        for var_property in var_props:
            variable = var_property [0]
            property = var_property [1]
            if variable in var_label_map: # We know the label of this variable
                label = var_label_map[variable]
                label_props_map = PropertiesValidator.__extend_dict_with_list_elements (label_props_map, label,  [property])
            else: #its a variable that we dont have a matched label (it will be inferred)
                var_props_map = PropertiesValidator.__extend_dict_with_list_elements (var_props_map, variable,  [property])
                    
        return  label_props_map, var_props_map   
    
    @staticmethod
    def __get_var_labels_props (query):
        '''
        It extracts from query vars, labels and props and returns the mapping:
        - variables with labels
        - labels with properties
        - unknown variables with properties
        Args:
            query(str): The query to be validated
        Returns
            Dict (var_label_map) that maps any variables with their labels 
            Dict (labels_props_map), that maps labels with properties they access
            Dict (var_props_map), that maps variables unmatched with any label, with the properties they access

        '''
        var_label_map, label_props_map = PropertiesValidator.__inline_var_label_properties_mapping(query)
        label_props_map, var_props_map = PropertiesValidator.__outside_var_properties_mapping(var_label_map, label_props_map,query)
        
        # print('var_label_map', var_label_map)
        # print('label_props_map',label_props_map)
        # print('var_props_map', var_props_map)
        return var_label_map, label_props_map, var_props_map
    
    @staticmethod
    def __extract_1hop_paths(query):
        ''' From a cypher query extract all the one hop paths and single nodes and return them as a list.
        If any multihop it breaks it into one hop paths

        Args:
            query(str): The query to be validated
        Returns:
            List of one hop paths (including single nodes, if any)
        '''

        # pattern of nodes
        node_pattern = r"\(\s*(?:\s*\w+\s*:\s*\w+\s*|\s*\w*\s*|:\s*\w+\s*|)\s*(?:\{[^}]*\})?\s*\)"
        # pattern of relationships
        rel_pattern = r"\[\s*(?:\s*\w+\s*:\s*\w+\s*|\s*\w*\s*|:\s*\w+\s*|)\s*(?:\{[^}]*\})?\s*\]"
        # combine node and relationships patterns
        path_pattern= rf'({node_pattern}\s*<?-\s*{rel_pattern}\s*->?\s*{node_pattern})'
        # A list containing the extracted paths (converted to one hop paths) and single nodes
        one_hop_paths = []

        #Find the patterns of 1 hop paths in the query 
        matches = re.findall(path_pattern,query,overlapped=True)

        nodes_in_paths = set() #Nodes taht appear in paths
        for path_match in matches:
            one_hop_paths.append(path_match)
            # extract all nodes in the path string
            nodes = re.findall(node_pattern, path_match)
            nodes_in_paths.update(nodes)

        # find all nodes
        all_node_matches = re.findall(node_pattern, query, overlapped=True)
        # filter out nodes that appear in paths
        single_node_matches = [node for node in all_node_matches if node not in nodes_in_paths]

        # Add single nodes to one_hop_paths
        one_hop_paths.extend(single_node_matches)

        return one_hop_paths

    @staticmethod
    def __prepare_query_for_infer (var_label_map, query):
        '''
        1. replace the known vars with their mapped label (so we dont infer them)
        2. Replace -- with -[]-
        3. Break query into one hop paths
        4. Remove from each 1 hop paths if any properties where accessed
        5. Create a list of 1 hop paths that have unknown variables to infer

        Args:
            Dict (var_label_map): that maps any variables with their labels 
            query(str): The query to be validated
        Returns:
            List of 1 hop paths that have unknown variables to infer 
        '''
        #replace the known vars with their mapped label
        query = replace_with_labels(query, var_label_map)

        # Replace -- with empty relationship
        query = query.replace("--", "-[]-")

        #Extract 1 hop paths 
        one_hop_paths = PropertiesValidator.__extract_1hop_paths(query)

        # Remove from each 1 hop paths if any properties where accessed
        # Regular expression to match properties inside curly braces (i.e., { })
        prop_pattern = r"\{[^}]*\}"
        no_prop_paths = [re.sub(prop_pattern, '', path) for path in one_hop_paths]

        # The final list with paths that have unknown variable and will be inferred
        inference_paths = []
        # Define the pattern for detecting unknown variables inside parentheses or square brackets
        pattern = r"\(\w+\)|\[\w+\]"
        # Filter the list to keep only elements that contain unknown variables
        inference_paths = [path for path in no_prop_paths if re.search(pattern, path)]

        return inference_paths