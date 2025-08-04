module mux_2_1 (
    input  [1:0] sel,
    input  [3:0] a,
    input  [3:0] b,
    output [3:0] c,
    output carry
);

    always @(a or b or sel) begin
        if (sel == 0) begin
            c = ~b;  
            carry = 0;
        end 
        else if (sel == 1) begin
            c = a & b;  
            carry = 0;|
        end
        else if (sel == 2) begin
            c = a | b;  
            carry = 0;|
        end
        else begin
            {carry:c} = a + b;  
            carry = 0;
        end
    end

endmodule
