module circuit_1 (
    input X,
    input Y,
    input Z,
    output W
);

assign W = (X | Y) & Z;

endmodule
