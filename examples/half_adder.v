module half_adder(
    input x,
    input y,
    output z,
    output c
); 

assign c = x & y;   // AND
assign z = x ^ y;   // XOR

endmodule
