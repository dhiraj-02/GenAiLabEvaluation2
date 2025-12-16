/*
Branch_predictor [14M]: Marking scheme: GHR module Instantiated [7M] {if GHR module marks in C are 0 then 0, if GHR module marks in C are 5 then 4, if GHR module marks in C are 10 then 7}, PHT module Instantiated [7M] {if PHT module marks in D are 0 or 4 then 0, if PHT module marks in D are 9 then 4, if PHT module marks in D are 14 then 7}
*/

// -----------------------------
// Top-level branch predictor
// -----------------------------
module branch_predictor (
    input  wire        clk,
    input  wire        reset,
    input  wire        update_en,
    input  wire        in_bit,
    output wire [2:0]  ghr_out,
    output wire [1:0]  pht_cnt,
    output wire        pred
);
    wire [2:0] ghr_internal;
    wire [1:0] pht_out_internal;

    GHR u_ghr (.clk(clk), .reset(reset), .update_en(update_en),
               .in_bit(in_bit), .ghr_out(ghr_internal));

    PHT u_pht (.clk(clk), .reset(reset), .update_en(update_en),
               .index(ghr_internal), .actual(in_bit), .pht_out(pht_out_internal));

    assign ghr_out = ghr_internal;
    assign pht_cnt = pht_out_internal;
    assign pred    = pht_out_internal[1];
endmodule