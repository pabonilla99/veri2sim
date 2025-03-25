module votador (input a,b,c,output z);
 assign z= (a & b) | (a & c) | (b & c);
endmodule