# agentmap/graph/   builder.py

"""
Graph builder for AgentMap.

Parses a CSV file to construct one or more workflow definitions.
Each workflow is identified by a unique GraphName.
"""

import csv
from collections import defaultdict
from pathlib import Path

from agentmap.exceptions.graph_exceptions import InvalidEdgeDefinitionError
from agentmap.logging import get_logger

logger = get_logger(__name__)


class Node:
    def __init__(self, name, context=None, agent_type=None, inputs=None, output=None, prompt=None):
        self.name = name
        self.context = context
        self.agent_type = agent_type
        self.inputs = inputs or []
        self.output = output
        self.prompt = prompt
        self.edges = {}  # condition: next_node

    def add_edge(self, condition, target_node):
        self.edges[condition] = target_node
        
    def has_conditional_routing(self):
        """Check if this node has conditional routing (success/failure paths)."""
        return "success" in self.edges or "failure" in self.edges

    def __repr__(self):
        edge_info = ", ".join([f"{k}->{v}" for k, v in self.edges.items()])
        return f"<Node {self.name} [{self.agent_type}] → {edge_info}>"


class GraphBuilder:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        logger.info(f"[GraphBuilder] Initialized with CSV: {self.csv_path}")
        self.graphs = defaultdict(dict)  # GraphName: { node_name: Node }

    def get_graph(self, name):
        return self.graphs.get(name, {})
    
    def _create_node(self, graph, node_name, context, agent_type, input_fields, output_field, prompt):
        """Create a new node with the given properties."""
        agent_type = agent_type or "Default"
        logger.trace(f"  ➕ Creating Node: graph: {graph}, node_name: {node_name}, context: {context} , agent_type: {agent_type}, input_fields: {input_fields}, output_field: {output_field}, prompt: {prompt}")
        # Only create if not already exists
        if node_name not in graph:
            graph[node_name] = Node(
                node_name, 
                context, 
                agent_type, 
                input_fields, 
                output_field, 
                prompt
            )
            logger.debug(f"  ➕ Created Node: {node_name} with agent_type: {agent_type}, output_field: {output_field}")
        else:
            logger.debug(f"  ⏩ Node {node_name} already exists, skipping creation")
            
        return graph[node_name]
    
    def _create_nodes_from_csv(self):
        """First pass: Create all nodes from CSV definitions."""
        row_count = 0
        
        with self.csv_path.open() as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                row_count += 1
                graph_name = row.get("GraphName", "").strip()
                node_name = row.get("Node", "").strip()
                context = row.get("Context", "").strip()
                agent_type = row.get("AgentType", "").strip()
                input_fields = [x.strip() for x in row.get("Input_Fields", "").split("|") if x.strip()]
                output_field = row.get("Output_Field", "").strip()
                prompt = row.get("Prompt", "").strip()
                
                logger.debug(f"[Row {row_count}] Processing: Graph='{graph_name}', Node='{node_name}', AgentType='{agent_type}'")
                
                if not graph_name:
                    logger.warning(f"[Line {row_count}] Missing GraphName. Skipping row.")
                    continue
                if not node_name:
                    logger.warning(f"[Line {row_count}] Missing Node. Skipping row.")
                    continue
                    
                # Get or create the graph
                graph = self.graphs[graph_name]
                
                # Create the node if it doesn't exist
                self._create_node(
                    graph, node_name, context, agent_type, 
                    input_fields, output_field, prompt
                )
        
        return row_count
    
    def _connect_nodes_with_edges(self):
        """Second pass: Connect nodes with edges."""
        with self.csv_path.open() as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                graph_name = row.get("GraphName", "").strip()
                node_name = row.get("Node", "").strip()
                edge_name = row.get("Edge", "").strip()
                success_next = row.get("Success_Next", "").strip()
                failure_next = row.get("Failure_Next", "").strip()
                
                if not graph_name or not node_name:
                    continue
                    
                graph = self.graphs[graph_name]
                
                # Check for conflicting edge definitions
                if edge_name and (success_next or failure_next):
                    logger.debug(f"  ⚠️ CONFLICT: Node '{node_name}' has both Edge and Success/Failure defined!")
                    raise InvalidEdgeDefinitionError(
                        f"Node '{node_name}' has both Edge and Success/Failure defined. "
                        f"Please use either Edge OR Success/Failure_Next, not both."
                    )
                
                # Connect with direct edge
                if edge_name:
                    self._connect_direct_edge(graph, node_name, edge_name, graph_name)
                
                # Connect with conditional edges
                elif success_next or failure_next:
                    if success_next:
                        self._connect_success_edge(graph, node_name, success_next, graph_name)
                    
                    if failure_next:
                        self._connect_failure_edge(graph, node_name, failure_next, graph_name)
    
    def _connect_direct_edge(self, graph, source_node, target_node, graph_name):
        """Connect nodes with a direct edge."""
        # Verify the edge target exists
        if target_node not in graph:
            logger.error(f"  ❌ Edge target '{target_node}' not defined in graph '{graph_name}'")
            raise ValueError(f"Edge target '{target_node}' is not defined as a node in graph '{graph_name}'")
        
        graph[source_node].add_edge("default", target_node)
        logger.debug(f"  🔗 {source_node} --default--> {target_node}")
    
    def _connect_success_edge(self, graph, source_node, target_node, graph_name):
        """Connect nodes with a success edge."""
        # Verify the success target exists
        if target_node not in graph:
            logger.error(f"  ❌ Success target '{target_node}' not defined in graph '{graph_name}'")
            raise ValueError(f"Success target '{target_node}' is not defined as a node in graph '{graph_name}'")
        
        graph[source_node].add_edge("success", target_node)
        logger.debug(f"  🔗 {source_node} --success--> {target_node}")
    
    def _connect_failure_edge(self, graph, source_node, target_node, graph_name):
        """Connect nodes with a failure edge."""
        # Verify the failure target exists
        if target_node not in graph:
            logger.error(f"  ❌ Failure target '{target_node}' not defined in graph '{graph_name}'")
            raise ValueError(f"Failure target '{target_node}' is not defined as a node in graph '{graph_name}'")
        
        graph[source_node].add_edge("failure", target_node)
        logger.debug(f"  🔗 {source_node} --failure--> {target_node}")
    
    def build(self):
        """Build all graphs from the CSV file."""
        if not self.csv_path.exists():
            logger.error(f"[GraphBuilder] CSV file not found: {self.csv_path}")
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Step 1: Create all nodes first
        row_count = self._create_nodes_from_csv()
        
        # Step 2: Connect nodes with edges
        self._connect_nodes_with_edges()
        
        logger.info(f"[GraphBuilder] Parsed {row_count} rows and built {len(self.graphs)} graph(s)")
        logger.debug(f"Graphs found: {list(self.graphs.keys())}")
        
        return self.graphs
    
    def print_graphs(self):
        for name, nodes in self.graphs.items():
            logger.debug(f"Graph: {name}")
            for node in nodes.values():
                logger.debug(f"  {node}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        logger.debug("Usage: python -m agentmap.graph.builder path/to/your.csv")
    else:
        gb = GraphBuilder(sys.argv[1])
        gb.build()
        gb.print_graphs()