module array_not (input [1:0]a, output [1:0] b);
    wire [1:0] v;
    assign v = ~a;
    assign b = v;
endmodule

