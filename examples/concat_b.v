module Concatenation #(parameter MAX = 8) (
    input [1:0] a,  // Entrada de 4 bits
    input [3:0] b,  // Entrada de 4 bits
    output [MAX-1:0] result // Salida de 8 bits (concatenación de a y b)
);
    assign result = {a, b, a}; 
endmodule