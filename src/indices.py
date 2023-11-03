
iSampleWeight       = 'WTMEC4YR'    # 4-year sample weight of the Mobile Examination Center
iSampleWeight05_06  = 'WTMEC2YR'    # 2-year sample weight of the Mobile Examination Center
 
iImpFlag        = 'DXITOT'          # The total number of imputations for the Dual-Energy X-ray Absorptiometry (DXA) whole body measures
iImpFlag05_06   = 'DXITOTBN'        # The total number of imputations for the Dual-Energy X-ray Absorptiometry (DXA) bone measures specifically

iSampleNo       = 'SEQN'            # In Paper  | In Formula
iWeight         = 'BMXWT'           # Weight    | we
iAge            = 'RIDAGEYR'        # Age       | o
iWaist          = 'BMXWAIST'        # Waist     | w
iHeight         = 'BMXHT'           # Height    | h
iBodyFatPct     = 'DXDTOPF'         # PBF       | pbf
iBodyFat        = 'DXDTOFAT'        # BF        | bf
iFatFreeMass    = 'DXDTOLE'         # FFM       | ffm
iTrunkFatPct    = 'DXDTRPF'         # TFP       | tfp
iSex            = 'RIAGENDR'        # Sex       | s
iBMICalc        = 'BMI'             # BMI       | bmi
iBMI            = 'BMXBMI'          # BMI       | bmi
iRace           = 'RIDRETH1'        # Race      | r
iArm            = 'BMXARMC'         # ARMC      | a
iTricep         = 'BMXTRI'          # TRI       | b
iThigh          = 'BMXTHICR'        # Thigh     | t
iSubscap        = 'BMXSUB'          # SUB       | ss
iCalf           = 'BMXCALF'         # CALF      | c
iArmLen         = 'BMXARML'         # ARM       | al        - check this
iLegLen         = 'BMXLEG'          # LEG       | l         - check this

iTrConsidered = [ iBodyFatPct, iSampleWeight, iSampleNo, iWeight, iAge, iWaist, iHeight,
                iSex, iBMICalc, iBMI, iRace, iArm, iTricep, iThigh, iSubscap, iCalf, iArmLen, iLegLen ]

iTeConsidered = [ iBodyFatPct, iSampleWeight05_06, iSampleNo, iWeight, iAge, iWaist, iHeight,
                iSex, iBMICalc, iBMI, iRace, iArm, iTricep, iThigh, iSubscap, iCalf, iArmLen, iLegLen ]
