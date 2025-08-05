module circuit_1_b (
    input X,
    input Y,
    input Z,
    output W
);

wire V;

assign V = X | Y;
assign W = V & Z;

endmodule
