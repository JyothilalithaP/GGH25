import re

def parse_verilog(verilog_code):
    """Parses Verilog code and extracts combinational logic as a dictionary."""
    graph = {}
    
    # Find all wire assignments (combinational logic)
    assignments = re.findall(r'assign\s+(\w+)\s*=\s*(.+);', verilog_code)
    
    for output, expr in assignments:
        # Extract signal dependencies (simple regex, assumes space separation)
        inputs = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
        
        graph[output] = [inp for inp in inputs if inp != output]
    
    return graph

def compute_combinational_depth(graph):
    """Computes the combinational depth using a DFS approach."""
    def dfs(node, visited, depth_cache):
        if node in depth_cache:
            return depth_cache[node]
        if node not in graph or not graph[node]:
            return 0  # Base case: input node has depth 0
        
        max_depth = 0
        for neighbor in graph[node]:
            if neighbor in visited:
                return float('inf')  # Cycle detected, return infinite depth
            visited.add(neighbor)
            max_depth = max(max_depth, dfs(neighbor, visited, depth_cache))
            visited.remove(neighbor)
        
        depth_cache[node] = max_depth + 1
        return depth_cache[node]
    
    depth_cache = {}
    max_depth = 0
    for node in graph:
        max_depth = max(max_depth, dfs(node, set(), depth_cache))
    
    return max_depth if max_depth != float('inf') else 0  # Return 0 if cycle detected

# Example Verilog code snippet
verilog_code = """
module example(input a, input b, input c, output f);
    wire d, e;
    assign d = a & b;
    assign e = d | c;
    assign f = e ^ b;
endmodule
"""

graph = parse_verilog(verilog_code)
combinational_depth = compute_combinational_depth(graph)
print(f"Combinational Depth: {combinational_depth}")
