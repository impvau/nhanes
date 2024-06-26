
iSampWeight     = 'SampleWeight'
iSampleWeight       = 'WTMEC4YR'    # 4-year sample weight of the Mobile Examination Center
iSampleWeight05_06  = 'WTMEC2YR'    # 2-year sample weight of the Mobile Examination Center
 
iImpFlag        = 'DXITOT'          # The total number of imputations for the Dual-Energy X-ray Absorptiometry (DXA) whole body measures
iImpFlag05_06   = 'DXITOTBN'        # The total number of imputations for the Dual-Energy X-ray Absorptiometry (DXA) bone measures specifically

iSampleNo       = 'SEQN'            # In Paper  | In Formula    | New Formula in paper
iWeight         = 'BMXWT'           # Weight    | we            | we
iAge            = 'RIDAGEYR'        # Age       | o             | ag
iWaist          = 'BMXWAIST'        # Waist     | wa            | wa
iHeight         = 'BMXHT'           # Height    | h             | h
iBodyFatPct     = 'DXDTOPF'         # PBF       | pbf
iBodyFat        = 'DXDTOFAT'        # BF        | bf
iFatFreeMass    = 'DXDTOLE'         # FFM       | ffm
iTrunkFatPct    = 'DXDTRPF'         # TFP       | tfp
iSex            = 'RIAGENDR'        # Sex       | s             
iBMICalc        = 'BMI'             # BMI       | bmi
iBMI            = 'BMXBMI'          # BMI       | bmi
iRace           = 'RIDRETH1'        # Race      | r
iArm            = 'BMXARMC'         # ARMC      | a             | ar
iTricep         = 'BMXTRI'          # TRI       | b             | tr
iThigh          = 'BMXTHICR'        # Thigh     | t             | th
iSubscap        = 'BMXSUB'          # SUB       | ss            | ss
iCalf           = 'BMXCALF'         # CALF      | c             | ca
iArmLen         = 'BMXARML'         # ARM       | al            | al
iLegLen         = 'BMXLEG'          # LEG       | l             | ll

iConsider       = [ iBodyFatPct, iSampWeight, iWeight, iAge, iWaist, iHeight,
                    iSex, iRace, iArm, iTricep, iThigh, iSubscap, iCalf, iArmLen, iLegLen 
                ]

iRename         = [ 'y', 'w', 'we', 'o', 'wa', 'h', 
                    's', 'r', 'a', 'b', 't', 'ss', 'c', 'al', 'l'
                ]