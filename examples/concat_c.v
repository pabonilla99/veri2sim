module Concatenation(
    input [1:0] a,  // Entrada de 4 bits
    input [1:0] b,  // Entrada de 4 bits
    output [7:0] result // Salida de 8 bits (concatenación de a y b)
);
    wire [1:0] x;
    assign x = a | b; 
    assign result = {x, a, 4'b11, b}; // a se coloca a la izquierda y b a la derecha
endmodule