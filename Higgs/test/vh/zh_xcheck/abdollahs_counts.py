
import sys

counts = {
    'mmtt'   : [5689 ,  68 ,  55 ,  ],
    'eett'   : [5120 ,  52 ,  45 ,  ],
    'mmmt'   : [366 ,   33 ,  14 ,  ],
    'eemt'   : [328 ,   28 ,  4 ,   ],
    'mmet'   : [226 ,   33 ,  9 ,   ],
    'eeet'   : [228 ,   46 ,  8 ,   ],
    'mmme'   : [15 ,    2 ,   3 ,   ],
    'eeem'   : [15 ,    2 ,   4 ,   ],
}

print counts[sys.argv[1]][int(sys.argv[2])]
