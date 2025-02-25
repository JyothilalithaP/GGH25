import re
from collections import defaultdict

def parse_verilog(verilog_code):
    """Extracts module connections and specifically tracks carry propagation."""
    connections = []
    
    # Regex pattern to match module instantiations
    gate_pattern = re.compile(r"(\w+)\s+(\w+)\s*\((.*?)\);")
    
    for match in gate_pattern.finditer(verilog_code):
        gate_type, gate_name, ports = match.groups()
        port_list = [p.strip().split('(')[-1].strip(')') for p in ports.split(',')]

        # Ensure we only process full adders
        if gate_type == "full_adder" and len(port_list) == 5:
            A, B, Cin, Sum, Cout = port_list
            connections.append((A, Sum))   # Sum output depends on A
            connections.append((B, Sum))   # Sum output depends on B
            connections.append((Cin, Sum)) # Sum output depends on Cin
            connections.append((Cin, Cout)) # Carry-out depends on carry-in
            connections.append((A, Cout))  # Carry-out depends on A
            connections.append((B, Cout))  # Carry-out depends on B
            
    return connections

def compute_critical_path(verilog_code):
    """Computes the longest combinational depth considering carry propagation."""
    connections = parse_verilog(verilog_code)
    graph = defaultdict(list)

    # Build the directed graph
    for src, dst in connections:
        graph[src].append(dst)

    # DFS function to compute depth
    def get_depth(node, memo={}):
        if node in memo:
            return memo[node]
        if node not in graph:
            return 0
        memo[node] = 1 + max((get_depth(neigh, memo) for neigh in graph[node]), default=0)
        return memo[node]

    # Compute the longest path in the graph
    max_depth = max((get_depth(node) for node in graph), default=0)
    return max_depth

# Example Verilog Code (Ripple Carry Adder)
verilog_code = """
module ripple_carry_adder(
    input [3:0] A, B,
    input Cin,
    output [3:0] Sum,
    output Cout
);
    wire c1, c2, c3;

    full_adder FA0(A[0], B[0], Cin, Sum[0], c1);
    full_adder FA1(A[1], B[1], c1, Sum[1], c2);
    full_adder FA2(A[2], B[2], c2, Sum[2], c3);
    full_adder FA3(A[3], B[3], c3, Sum[3], Cout);

endmodule

module full_adder(
    input A, B, Cin,
    output Sum, Cout
);
    assign Sum = A ^ B ^ Cin;
    assign Cout = (A & B) | (B & Cin) | (A & Cin);
endmodule
"""

# Run Analysis
critical_depth = compute_critical_path(verilog_code)
print(f"Predicted Combinational Depth: {critical_depth}")
