#!/usr/bin/env python3
##############################################################################
## This file is part of 'ATLAS ALTIROC DEV'.
## It is subject to the license terms in the LICENSE.txt file found in the
## top-level directory of this distribution and at:
##    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html.
## No part of 'ATLAS ALTIROC DEV', including this file,
## may be copied, modified, propagated, or distributed except according to
## the terms contained in the LICENSE.txt file.
##############################################################################

import pyrogue as pr
import common

class AltirocSlowControl(pr.Device):
    def __init__(
        self,
        name        = "AltirocSlowControl",
        description = "Container for Altiroc ASIC's slow control shift register",
        asicVersion = 2,
            **kwargs):

        super().__init__(name=name,description=description,**kwargs)

        downToBitOrdering = pr.UIntReversed
        upToBitOrdering   = pr.UInt

        def addReg(name,description,bitSize,bitOffset,value,base):

            remap = divmod((bitOffset-1),32)

            self.add(pr.RemoteVariable(
                name        = name,
                description = description,
                base        = base,
                offset      = (remap[0]<<2),
                mode        = 'RW',
                bitSize     = bitSize,
                bitOffset   = remap[1],
                # value       = value,
            ))

        addReg(
            name        = 'dac',
            description = 'ALTLAS LARG DAC',
            bitSize     = 10,
            bitOffset   = 1,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'ON_dac_LR',
            description = 'Undefined',
            bitSize     = 1,
            bitOffset   = 11,
            value       = 0x1, # DEF Value
            base        = downToBitOrdering,
        )

        ##############
        # bias_channel
        ##############

        addReg(
            name        = 'Write_opt',
            description = 'SRAM',
            bitSize     = 1,
            bitOffset   = 12,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'Precharge_opt',
            description = 'SRAM',
            bitSize     = 1,
            bitOffset   = 13,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'ref_bg',
            description = 'Bandgap',
            bitSize     = 1,
            bitOffset   = 14,
            value       = 0x1, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'dac_pulser',
            description = 'Internal pulser',
            bitSize     = 6,
            bitOffset   = 15,
            value       = 0x7, # DEF Value
            base        = downToBitOrdering,
        )

        ############################################

        if( asicVersion <= 2 ):

            addReg(
                name        = 'Ccomp_TZ',
                description = 'for TZ preamp only',
                bitSize     = 1,
                bitOffset   = 21,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        else:

            addReg(
                name        = 'ON_rtest',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 21,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        ############################################

        addReg(
            name        = 'Rin_Vpa',
            description = 'DEF=25K Vpa only',
            bitSize     = 1,
            bitOffset   = 22,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'Cp_Vpa',
            description = 'Cpole VPA preamp',
            bitSize     = 3,
            bitOffset   = 23,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'dac_biaspa',
            description = 'Id input trans',
            bitSize     = 6,
            bitOffset   = 26,
            value       = 0xC, # DEF Value
            base        = downToBitOrdering,
        )

        ############################################

        if( asicVersion <= 2 ):

            addReg(
                name        = 'ON_dac_biaspa',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 32,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

        ############################################

        addReg(
            name        = 'ON_ota_dac',
            description = 'Undefined',
            bitSize     = 1,
            bitOffset   = 33,
            value       = 0x1, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'DAC10bit',
            description = '10 bit DAC to set Vth (Treshold)',
            bitSize     = 10,
            bitOffset   = 34,
            value       = 0x80, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'SatFVa',
            description = 'TDC VPA',
            bitSize     = 3,
            bitOffset   = 44,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        addReg(
            name        = 'IntFVa',
            description = 'Undefined',
            bitSize     = 3,
            bitOffset   = 47,
            value       = 0x0, # DEF Value
            base        = downToBitOrdering,
        )

        ############################################

        if( asicVersion <= 2 ):

            addReg(
                name        = 'SatFTz',
                description = 'TDC TZ',
                bitSize     = 3,
                bitOffset   = 50,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'IntFTz',
                description = 'Undefined',
                bitSize     = 3,
                bitOffset   = 53,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'totf_satovfw',
                description = 'TOT fine',
                bitSize     = 1,
                bitOffset   = 56,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        else:

            addReg(
                name        = 'EN_toa_busy',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 50,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'ON_ota_dll',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 51,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_clps',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 52,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'totf_satovfw',
                description = 'TOT fine',
                bitSize     = 1,
                bitOffset   = 54,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'totc_satovfw',
                description = 'TOT coarse',
                bitSize     = 1,
                bitOffset   = 55,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'toac_satovfw',
                description = 'TOA overflow',
                bitSize     = 1,
                bitOffset   = 56,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        ################################################
        # Note: These are V2 (or earlier) only registers
        ################################################

        if( asicVersion <= 2 ):

            addReg(
                name        = 'totc_satovfw',
                description = 'TOT coarse',
                bitSize     = 1,
                bitOffset   = 57,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'toa_satovfw',
                description = 'TOA overflow',
                bitSize     = 1,
                bitOffset   = 58,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'Ck40_choice',
                description = '40MHz choice',
                bitSize     = 1,
                bitOffset   = 59,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cBitf',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 60,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'DLL_ALockR_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 64,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'CP_b',
                description = 'Undefined',
                bitSize     = 3,
                bitOffset   = 65,
                value       = 0x3, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'ext_Vcrtlf_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 68,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cBits',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 69,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'ext_Vcrtls_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 73,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cBitc',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 74,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'ext_Vcrtlc_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 78,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'en_8drivers',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 79,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        ############################################

        ######################
        # Pixel Configurations
        ######################

        if( asicVersion <= 2 ):

            pixChBitOffset = [80,113,146,179,215,248,281,314,347,383,416,449,482,515,551,584,617,650,683,719,752,785,818,851,887]

        else:

            pixChBitOffset = [57, 90,123,156,192,225,258,291,324,360,393,426,459,492,528,561,594,627,660,696,729,762,795,828,864]

        ############################################

        for i in range(25):

            addReg(
                name        = f'EN_ck_SRAM[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (0+pixChBitOffset[i]),
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'ON_Ctest[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (1+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'disable_pa[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (2+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'bit_vth_cor[{i}]',
                description = 'Undefined',
                bitSize     = 7,
                bitOffset   = (3+pixChBitOffset[i]),
                value       = 0x8, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'ON_discri[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (10+pixChBitOffset[i]),
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'EN_hyst[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (11+pixChBitOffset[i]),
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'EN_trig_ext[{i}]',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = (12+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            ############################################

            if( asicVersion <= 2 ):

                addReg(
                    name        = f'cBit_f_TOT[{i}]',
                    description = 'Undefined',
                    bitSize     = 4,
                    bitOffset   = (13+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

            else:

                addReg(
                    name        = f'en_rstb_toa[{i}]',
                    description = 'TOA TDC under reset when en_rstb=1',
                    bitSize     = 1,
                    bitOffset   = (13+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

                addReg(
                    name        = f'cBit_f_TOT[{i}]',
                    description = 'Undefined',
                    bitSize     = 3,
                    bitOffset   = (14+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

            ############################################

            addReg(
                name        = f'cBit_c_TOT[{i}]',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = (17+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            ############################################

            if( asicVersion <= 2 ):

                addReg(
                    name        = f'cBit_s_TOT[{i}]',
                    description = 'Undefined',
                    bitSize     = 4,
                    bitOffset   = (21+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

            else:

                addReg(
                    name        = f'en_rstb_tot[{i}]',
                    description = 'TOT TDC under reset when en_rstb=1',
                    bitSize     = 1,
                    bitOffset   = (21+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

                addReg(
                    name        = f'cBit_s_TOT[{i}]',
                    description = 'Undefined',
                    bitSize     = 3,
                    bitOffset   = (22+pixChBitOffset[i]),
                    value       = 0x0, # DEF Value
                    base        = downToBitOrdering,
                )

            ############################################

            addReg(
                name        = f'cBit_s_TOA[{i}]',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = (25+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = f'cBit_f_TOA[{i}]',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = (29+pixChBitOffset[i]),
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

        ############################################

        if( asicVersion <= 2 ):

            cdBitOffset = [212,380,548,716,884]
            cdDefine    = 'In units of 0.5pF',

        else:

            cdBitOffset = [189,357,525,693,861]
            cdDefine    = 'In units of 1.0pF',

        ############################################

        for i in range(5):

            addReg(
                name        = f'cd[{i}]',
                description = '',
                bitSize     = 3,
                bitOffset   = cdBitOffset[i],
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

        ############################################

        if( asicVersion <= 2 ):

            ###############
            # Phase shifter
            ###############

            addReg(
                name        = 'PLL',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 920,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'dac_icpb',
                description = 'Undefined',
                bitSize     = 6,
                bitOffset   = 921,
                value       = 0xA, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'Shifted_ck40',
                description = 'Was dac_CP_BW<0> in V1',
                bitSize     = 1,
                bitOffset   = 927,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'dac_CP_BWb',
                description = 'Undefined',
                bitSize     = 5,
                bitOffset   = 928,
                value       = 0x20, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_Ext_Vin_VCO',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 933,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'setN',
                description = 'Undefined',
                bitSize     = 2,
                bitOffset   = 934,
                value       = 0x3, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'setProbe',
                description = 'Undefined',
                bitSize     = 3,
                bitOffset   = 936,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_500',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 939,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_1000',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 940,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_2000',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 941,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_4000',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 942,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_200p',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 943,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_LowKvco',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 944,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            ####################
            # 640M_Phase shifter
            ####################

            addReg(
                name        = 'delay',
                description = 'Undefined',
                bitSize     = 8,
                bitOffset   = 945,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'Ph',
                description = 'Change internal clock from PLL or external input',
                bitSize     = 2,
                bitOffset   = 953,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'forcedown',
                description = 'DLL force down',
                bitSize     = 1,
                bitOffset   = 955,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'inita',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 956,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'initb',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 957,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'initc',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 958,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cpen',
                description = 'Charge pump bias enable',
                bitSize     = 1,
                bitOffset   = 959,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cp',
                description = 'charge pump current adjust.',
                bitSize     = 4,
                bitOffset   = 960,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'En_40M',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 964,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'En_640M',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 965,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

        ########################################
        #           asicVersion = 3
        ########################################
        else:

            ########################################
            #             DLL SC
            ########################################

            addReg(
                name        = 'choice_shifted_ck40',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 897,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'choice_fpga_ck40',
                description = '1 => FPGA ck40 used, whatever choice_shifted_ck40',
                bitSize     = 1,
                bitOffset   = 898,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'cBitf',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 899,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'DLLfast_EXTvctrl_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 903,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'fast_Lcomp_b',
                description = 'New SC for Fast DLL: Leakage I compensation DEF= 48 but to be set to 0',
                bitSize     = 6,
                bitOffset   = 904,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'fast_Up_Downb',
                description = 'New SC for Fast DLL',
                bitSize     = 1,
                bitOffset   = 910,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'DLL_CP_b',
                description = 'DLL Charge pump I: 2 additional bits in V3, CP_b<4>: DEF=0 but to be set to 1',
                bitSize     = 5,
                bitOffset   = 911,
                value       = 0x10, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'DLL_ALockR_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 916,
                value       = 0x1, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'Cbits',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 917,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'DLLslow_EXTvctrl_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 921,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'slow_Lcomp_b',
                description = 'New SC for Slow DLL: Leakage I compensation DEF= 12 but to be set to 0',
                bitSize     = 6,
                bitOffset   = 922,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'slow_Up_Downb',
                description = 'New SC for Slow DLL',
                bitSize     = 1,
                bitOffset   = 928,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'Cbitc',
                description = 'Undefined',
                bitSize     = 4,
                bitOffset   = 929,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'DLLcoarse_EXTvctrl_en',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 933,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'coarse_Lcomp_b',
                description = 'New SC for coarse DLL: Leakage I compensation DEF=0',
                bitSize     = 6,
                bitOffset   = 934,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'coarse_Up_Downb',
                description = 'New SC for Coarse DLL',
                bitSize     = 1,
                bitOffset   = 940,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            addReg(
                name        = 'EN_8drivers',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 941,
                value       = 0x0, # DEF Value
                base        = downToBitOrdering,
            )

            ########################################
            # PLL_PSV4_RPG: PLL_SC/ PLL Slow Control
            ########################################

            addReg(
                name        = 'ON PLL',
                description = 'Undefined',
                bitSize     = 1,
                bitOffset   = 942,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'PLL_icpb',
                description = 'PLL Charge pump I, was named dac_icpb<i>',
                bitSize     = 6,
                bitOffset   = 943,
                value       = 0x0A, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_RPG',
                description = 'was shifted_ck40 in V2, SC used/renamed in V3 for Random Generator (Freq set by 10-bit RPG DAC and SetProbe<2:0>)',
                bitSize     = 1,
                bitOffset   = 949,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'dac_CP_BWb',
                description = 'PLL BW',
                bitSize     = 5,
                bitOffset   = 950,
                value       = 0x10, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_ExtVin_vco_PLL',
                description = 'PLL external voltage for vco (was named EN_ExtVin_VCO)',
                bitSize     = 1,
                bitOffset   = 955,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'setN',
                description = 'PLL SC, setN<0:1>: set PLL feedback freq. (0 => 40 MHz, 3=> 320 MHz)',
                bitSize     = 2,
                bitOffset   = 956,
                value       = 0x3, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'setProbe',
                description = 'PLL SC, was 0 in V2, SetProbe = 5 => Probe_ck= vco32=PLL 40 MHz, setProbe also used to select probe_ck(vco) for RPG. SetProbe=0: vco=1.28 GHz',
                bitSize     = 3,
                bitOffset   = 958,
                value       = 0x5, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_500',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 961,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_1000',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 962,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_2000',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 963,
                value       = 0x1, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_4000',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 964,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_200p',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 965,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'EN_LowKvco',
                description = 'PLL SC',
                bitSize     = 1,
                bitOffset   = 966,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            ########################################
            # PLL_PSV4_RPG: Phase Shifter SC
            ########################################

            addReg(
                name        = 'FineDelay',
                description = 'Phase Shifter SC, was named delay<0> in V2, LSB =97 ps',
                bitSize     = 4,
                bitOffset   = 967,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'CoarseDelay',
                description = 'was named delay<4> in V2 (coarse), LSB=1.6 ns',
                bitSize     = 4,
                bitOffset   = 971,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'p',
                description = 'Undefined',
                bitSize     = 2,
                bitOffset   = 975,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'forcedown',
                description = 'DLL force down',
                bitSize     = 1,
                bitOffset   = 977,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'inita',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 978,
                value       = 0x1, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'initb',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 979,
                value       = 0x1, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'initc',
                description = 'Initial Vbias',
                bitSize     = 1,
                bitOffset   = 980,
                value       = 0x1, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'cpen',
                description = 'Charge pump bias enable',
                bitSize     = 1,
                bitOffset   = 981,
                value       = 0x1, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'PS_cp',
                description = 'Phase shifter charge pump current, was named cp<i> in V2',
                bitSize     = 4,
                bitOffset   = 982,
                value       = 0x8, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'En_40M',
                description = 'use of internal PLL 40MHz',
                bitSize     = 1,
                bitOffset   = 986,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'En_640M',
                description = 'use of internal PLL 640MHz',
                bitSize     = 1,
                bitOffset   = 987,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'FineDelayLum',
                description = 'Phase Shifter SC',
                bitSize     = 4,
                bitOffset   = 988,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

            addReg(
                name        = 'detectEn',
                description = 'Phase Shifter SC',
                bitSize     = 1,
                bitOffset   = 992,
                value       = 0x0, # DEF Value
                base        = upToBitOrdering,
            )

        ############################################

        self.add(pr.RemoteVariable(
            name         = 'SHIFT_REG_SIZE_G',
            description  = 'Number of bits in the shift register',
            offset       = 0xFF8,
            bitSize      = 32,
            mode         = 'RO',
            disp         = '{:d}',
        ))

        self.add(pr.RemoteVariable(
            name         = 'rstL',
            description  = 'Shift Register\'s reset (active LOW)',
            offset       = 0xFFC,
            bitSize      = 1,
            mode         = 'RW',
            base         = pr.UInt,
            value       = 0x1,
        ))
