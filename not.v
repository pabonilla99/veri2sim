module not_not (input a,
                input [1:0] b,
                output c,
                output [1:0] d );
    wire w;
    wire [1:0] v;
    assign w = ~a;
    assign c = w;
    assign v = ~b;
    assign d = v;
endmodule

