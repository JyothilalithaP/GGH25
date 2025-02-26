# GGH25
AI algorithm to predict combinational complexity/depth of signals to quickly identify timing violations.
# Verilog Combinational Depth Analyzer

## Overview
This project provides a Python script to analyze the **combinational depth** of a given Verilog code. Instead of running full synthesis, the script parses `assign` statements, constructs a **data flow graph**, and computes the longest combinational path (depth) using **Depth-First Search (DFS)**.

## What is Combinational Depth?
Combinational depth (also called **logic depth**) refers to the **longest sequence of logic gates** a signal must travel through before reaching an output. It directly affects **propagation delay**, which in turn limits the maximum clock speed of a circuit.

For example, consider this Verilog logic:
```verilog
assign d = a & b;  // Level 1
assign e = d | c;  // Level 2
assign f = e ^ b;  // Level 3
```
Here, `f` depends on `e`, which depends on `d`, leading to a **combinational depth of 3**.

## Understanding Time Delays
In digital circuits, time delay is caused by **gate propagation delays**. Each logic gate takes some time to process inputs and produce an output. The **critical path** (longest combinational path) determines the **worst-case delay**, limiting how fast the circuit can operate.

Formula for **maximum clock frequency**:
```
Max Frequency = 1 / (Critical Path Delay)
```
By optimizing combinational depth, we can **reduce delay and increase performance**. This script helps analyze and estimate depth before synthesis.

## How It Works
1. The script extracts **combinational assignments** (`assign` statements) from Verilog code.
2. It builds a **directed graph** where signals are nodes and assignments form edges.
3. It runs a **DFS-based longest path search** to compute combinational depth.
4. If a cycle is detected, the script assumes invalid combinational logic.

## Example Verilog Code for Testing
Insert this example code instead of the given code in the main script to check and verify the functionality:
```verilog
module test(input a, input b, input c, input d, output y);
    wire w1, w2, w3, w4;
    assign w1 = a & b;
    assign w2 = w1 | c;
    assign w3 = w2 ^ d;
    assign w4 = w3 & a;
    assign y = w4 | b;
endmodule
```
Expected Output:
```bash
Combinational Depth: 5
```
This means the longest signal path from input to output has **5 logic levels**.

## Why Use This?
- Fast pre-synthesis depth analysis  
- Helps identify timing bottlenecks  
- No need for full synthesis tools  
- Easily test and debug Verilog logic  

---

