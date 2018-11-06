-------------------------------------------------------------------------------
-- File       : AtlasAltirocClk.vhd
-- Company    : SLAC National Accelerator Laboratory
-- Created    : 2018-09-07
-- Last update: 2018-11-01
-------------------------------------------------------------------------------
-- Description: PLL Wrapper and 160 MHz clock MUX
-------------------------------------------------------------------------------
-- This file is part of 'ATLAS ALTIROC DEV'.
-- It is subject to the license terms in the LICENSE.txt file found in the 
-- top-level directory of this distribution and at: 
--    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
-- No part of 'ATLAS ALTIROC DEV', including this file, 
-- may be copied, modified, propagated, or distributed except according to 
-- the terms contained in the LICENSE.txt file.
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;

use work.StdRtlPkg.all;

library unisim;
use unisim.vcomponents.all;

entity AtlasAltirocClk is
   generic (
      TPD_G        : time    := 1 ns;
      SIMULATION_G : boolean := false);
   port (
      -- Jitter Cleaner PLL Ports
      localRefClkP : in  sl;
      localRefClkN : in  sl;
      pllClkOutP   : out sl;
      pllClkOutN   : out sl;
      pllClkInP    : in  slv(3 downto 0);
      pllClkInN    : in  slv(3 downto 0);
      pllSpiRstL   : out sl;
      pllSpiOeL    : out sl;
      pllClkSel    : out slv(1 downto 0);
      pllIntrL     : in  sl;
      pllLolL      : in  sl;
      -- Status/Config Interface
      axilClk      : in  sl;
      axilRst      : in  sl;
      clkSel       : in  slv(1 downto 0);
      oscOe        : out slv(3 downto 0);
      pwrSyncSclk  : out sl;
      pwrSyncFclk  : out sl;
      pllLocked    : out sl;
      -- Reference Clock/Reset Interface
      deserClk     : out sl;
      deserRst     : out sl;
      clk160MHz    : out sl;
      rst160MHz    : out sl);
end AtlasAltirocClk;

architecture mapping of AtlasAltirocClk is

   signal localRefClock : sl;
   signal localRefClk   : sl;
   signal pllClkIn      : slv(3 downto 0);
   signal refClk        : sl;
   signal deserClock    : sl;

begin

   pllClkSel <= clkSel;

   U_pllLocked : entity work.Synchronizer
      generic map (
         TPD_G => TPD_G)
      port map (
         clk     => axilClk,
         dataIn  => pllLolL,
         dataOut => pllLocked);

   --------------------------------------------   
   -- On-board 160 MHz reference for SI5345 PLL
   --------------------------------------------      
   U_IBUFDS : IBUFDS_GTE2
      port map (
         I     => localRefClkP,
         IB    => localRefClkN,
         CEB   => '0',
         ODIV2 => open,
         O     => localRefClock);

   U_localRefClk : BUFG
      port map (
         I => localRefClock,
         O => localRefClk);

   U_ClkOutBufDiff : entity work.ClkOutBufDiff
      generic map (
         TPD_G => TPD_G)
      port map (
         clkIn   => localRefClk,
         clkOutP => pllClkOutP,
         clkOutN => pllClkOutN);

   ---------------------------------
   -- FPGA_CLK_IN[3:1] Input buffers
   ---------------------------------
   GEN_VEC : for i in 3 downto 0 generate
      U_IBUFDS : IBUFDS
         port map (
            I  => pllClkInP(i),
            IB => pllClkInN(i),
            O  => pllClkIn(i));
   end generate GEN_VEC;

   -----------------------------------------   
   -- External Trigger/CMD Pulse Clock/Reset
   -----------------------------------------   
   U_refClk : BUFG
      port map (
         I => pllClkIn(0),
         O => refClk);

   clk160MHz <= refClk;

   U_refRst : entity work.PwrUpRst
      generic map(
         TPD_G          => TPD_G,
         IN_POLARITY_G  => '0',
         OUT_POLARITY_G => '1',
         SIM_SPEEDUP_G  => SIMULATION_G)
      port map (
         arst   => pllLolL,
         clk    => refClk,
         rstOut => rst160MHz);

   ---------------------------
   -- Deserializer Clock/Reset
   ---------------------------
   U_deserClock : BUFG
      port map (
         I => pllClkIn(1),
         O => deserClock);

   deserClk <= deserClock;

   U_deserRst : entity work.PwrUpRst
      generic map(
         TPD_G          => TPD_G,
         IN_POLARITY_G  => '0',
         OUT_POLARITY_G => '1',
         SIM_SPEEDUP_G  => SIMULATION_G)
      port map (
         arst   => pllLolL,
         clk    => deserClock,
         rstOut => deserRst);

   ----------------------------------------------
   -- Not synchronizing the DC/DC to system clock
   ----------------------------------------------
   pwrSyncSclk <= '0';
   pwrSyncFclk <= '0';

   ---------------------
   -- OSC Always enabled
   ---------------------
   oscOe <= x"F";

   ------------------------
   -- PLL OE Always enabled
   ------------------------
   pllSpiOeL <= '0';

   -----------------------------------------------------
   -- Reset SPI interface with respect to AXI-Lite reset
   -----------------------------------------------------
   pllSpiRstL <= not(axilRst);

end mapping;