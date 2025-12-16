`timescale 1ns/1ps

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



/*
PHT [14M]: Marking scheme: Initialization { Incomplete initialization - 0M Correct initialization - 4M}, PHT_table counter update logic and reset values {Arbitary code - 0, Partially correct code - 5M, Completely correct - 10M}
*/
// -----------------------------
// PHT module (combinational read, synchronous update)
// -----------------------------
module PHT (
    input  wire        clk,
    input  wire        reset,
    input  wire        update_en,
    input  wire [2:0]  index,
    input  wire        actual,
    output reg  [1:0]  pht_out
);
    reg [1:0] pht_array [0:7];
    integer i;

    // Combinational read (pre-update view)
    always @(*) begin
        pht_out = pht_array[index];
    end

    // Synchronous reset + update
    always @(posedge clk) begin
        if (reset) begin
            for (i = 0; i < 8; i = i + 1)
                pht_array[i] <= 2'b10;  // Weakly Taken
        end else if (update_en) begin
            if (actual) begin
                if (pht_array[index] != 2'b11)
                    pht_array[index] <= pht_array[index] + 1'b1;
            end else begin
                if (pht_array[index] != 2'b00)
                    pht_array[index] <= pht_array[index] - 1'b1;
            end
        end
    end
endmodule



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



/*
Test_bench [12M]: Marking scheme: Arbitary/Illogical code - 0M, Some meaningful partial code - 4M, Correct Output generating - 12M  
*/

// -----------------------------
// Testbench (fixed initialization & sampling timing)
// -----------------------------
module tb_branch_predictor;
    reg clk, reset, update_en, in_bit;
    wire [2:0] ghr;
    wire [1:0] pht_cnt;
    wire       pred;

    branch_predictor DUT (.clk(clk), .reset(reset), .update_en(update_en),
                          .in_bit(in_bit), .ghr_out(ghr), .pht_cnt(pht_cnt),
                          .pred(pred));

    reg [0:27] trace_bits;
    integer i, total, correct;
    reg [1:0] pht_before, pht_after;
    reg [2:0] ghr_before;

    // Clock generation (10 ns period)
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        // Branch trace: T T N T N N T T T N N T N T T T N T N N T T T N N T N T
        trace_bits = 28'b1_1_0_1_0_0_1_1_1_0_0_1_0_1_1_1_0_1_0_0_1_1_1_0_0_1_0_1;
        total = 0; correct = 0;

        // Apply reset for multiple clock cycles to ensure synchronous initialization
        reset = 1;
        update_en = 0;
        in_bit = 0;

        // Wait two rising edges while reset=1 so all regs are initialized on posedge
        @(posedge clk);
        @(posedge clk);

        // Now release reset, wait one more rising edge so combinational reads settle
        reset = 0;
        @(posedge clk);
        #1; // allow combinational outputs (pht_cnt) to settle

        $display("Cycle  GHR  PHT_cnt  PHT_upd  Pred  Actual  Total  Correct");

        // Main loop: for each branch, sample pre-update state, apply update, then sample post-update
        for (i = 0; i < 28; i = i + 1) begin
            // PRE-UPDATE sample (GHR and pre-update PHT counter are valid now)
            ghr_before = ghr;         // stable because we waited after reset
            pht_before = pht_cnt;     // combinational read for current GHR

            // apply actual and enable update for the next posedge
            in_bit = trace_bits[i];
            update_en = 1;

            // next rising edge performs the synchronous update (PHT entry and GHR shift)
            @(posedge clk);
            #1; // let synchronous updates and combs settle

            // POST-UPDATE: read the updated PHT entry for the old index (ghr_before)
            // We read internal array to capture the updated value (post-update)
            pht_after = DUT.u_pht.pht_array[ghr_before];

            // Statistics: prediction compares pre-update MSB with actual
            total = total + 1;
            if (pht_before[1] == in_bit) correct = correct + 1;

            // Display exactly like the question paper sample
            $display("%2d     %03b    %02b       %02b      %b      %b      %2d      %2d",
                     i, ghr_before, pht_before, pht_after, pht_before[1],
                     in_bit, total, correct);

            // clear update enable for next cycle
            update_en = 0;
            in_bit = 0;

            // wait a small time or a negative edge to align loop timing
            @(negedge clk);
        end

        $display("Simulation complete. Final accuracy = %0d / %0d", correct, total);
        $finish;
    end
endmodule