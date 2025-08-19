module Concatenation(
    input [1:0] a,  // Entrada de 2 bits
    input [3:0] b,  // Entrada de 4 bits
    output [7:0] result // Salida de 8 bits (concatenación de a y b)
);
    // Concatenación de las dos entradas
    assign result = {a, b, a}; // a se coloca a la izquierda y b a la derecha
endmodule