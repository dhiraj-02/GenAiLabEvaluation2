/*
GHR [10M]: Marking scheme: [0/5/10] Incomplete or arbitary code- 0M, Partially correct and/or shifting logic attmepted - 5M, Correct code:10M   
*/
module GHR (
    input  wire clk,
    input  wire reset,
    input  wire update_en,
    input  wire in_bit,
    output reg  [2:0] ghr_out
);
    always @(posedge clk) begin
        if (reset)
            ghr_out <= 3'b000;
        else if (update_en)
            ghr_out <= {ghr_out[1:0], in_bit};
    end
endmodule