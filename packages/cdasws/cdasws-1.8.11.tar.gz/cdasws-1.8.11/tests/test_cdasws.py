#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://cdaweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2019-2024 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the CdasWs class.<br>

Copyright &copy; 2019-2024 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import unittest
import re
import json

from datetime import datetime
from typing import Dict
from context import cdasws  # pylint: disable=unused-import

# pylint: enable=import-error,wrong-import-position
from cdasws import CdasWs
#from cdasws.cdasws import CdasWs
from cdasws.timeinterval import TimeInterval
from cdasws.datarequest import GraphOptions, ImageFormat, Overplot
# pylint: enable=import-error,wrong-import-position


# pylint: disable=line-too-long

BALLOONS_OBSERV_GROUP = [
        {
            "Name": "Balloons",
            "ObservatoryId": [
                "PMC Turbo",
                "bar_1A",
                "bar_1B",
                "bar_1C",
                "bar_1D",
                "bar_1G",
                "bar_1H",
                "bar_1I",
                "bar_1J",
                "bar_1K",
                "bar_1M",
                "bar_1N",
                "bar_1O",
                "bar_1Q",
                "bar_1R",
                "bar_1S",
                "bar_1T",
                "bar_1U",
                "bar_1V",
                "bar_2A",
                "bar_2B",
                "bar_2C",
                "bar_2D",
                "bar_2E",
                "bar_2F",
                "bar_2I",
                "bar_2K",
                "bar_2L",
                "bar_2M",
                "bar_2N",
                "bar_2O",
                "bar_2P",
                "bar_2Q",
                "bar_2T",
                "bar_2W",
                "bar_2X",
                "bar_2Y",
                "bar_3A",
                "bar_3B",
                "bar_3C",
                "bar_3D",
                "bar_3E",
                "bar_3F",
                "bar_3G",
                "bar_4A",
                "bar_4B",
                "bar_4C",
                "bar_4D",
                "bar_4E",
                "bar_4F",
                "bar_4G",
                "bar_4H",
                "bar_5A",
                "bar_6A",
                "bar_7A"
            ]
        }
    ]


APOLLO12_SWS_1HR = {
    "Id": "APOLLO12_SWS_1HR",
    "Doi": "10.48322/vars-pj10",
    "SpaseResourceId": "spase://NASA/NumericalData/Apollo12-LM/SWS/PT1HR",
    "Observatory": [
        "ALSEP"
    ],
    "Instrument": [
        "SWS"
    ],
    "ObservatoryGroup": [
        "Apollo"
    ],
    "InstrumentType": [
        "Particles (space)",
        "Plasma and Solar Wind"
    ],
    "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
    "TimeInterval": {
        "Start": "1969-11-19T19:30:00.000Z",
        "End": "1976-03-25T08:30:00.000Z"
    },
    "PiName": "Conway W. Snyder",
    "PiAffiliation": "Jet Propulsion Laboratory ",
    "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_1HR",
    "DatasetLink": [
        {
            "Title": "Documentation",
            "Text": "Dataset ",
            "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
        },
        {
            "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
            "Text": "Additional Data Services via",
            "Url": "https://lunasox.gsfc.nasa.gov"
        }
    ],
    "AdditionalMetadata": [
        {
            "Type": "SPASE",
            "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo12-LM/SWS/PT1HR"
        },
        {
            "Type": "SPDF_SKT_CDF",
            "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo12_sws_1hr_00000000_v01.json"
        }
    ]
}

APOLLO12_SWS_1HR_DATASETS = [
    APOLLO12_SWS_1HR
]

APOLLO_SWP_DATASETS = [
    APOLLO12_SWS_1HR,
    {
        "Id": "APOLLO12_SWS_28S",
        "Doi": "10.48322/wh21-c403",
        "SpaseResourceId": "spase://NASA/NumericalData/Apollo12-LM/SWS/PT28S",
        "Observatory": [
            "ALSEP"
        ],
        "Instrument": [
            "SWS"
        ],
        "ObservatoryGroup": [
            "Apollo"
        ],
        "InstrumentType": [
            "Particles (space)",
            "Plasma and Solar Wind"
        ],
        "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
        "TimeInterval": {
            "Start": "1969-11-19T18:42:13.000Z",
            "End": "1976-03-25T08:35:57.000Z"
        },
        "PiName": "Conway W. Snyder",
        "PiAffiliation": "Jet Propulsion Laboratory ",
        "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_28S",
        "DatasetLink": [
            {
                "Title": "Documentation",
                "Text": "Dataset ",
                "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
            },
            {
                "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                "Text": "Additional Data Services via",
                "Url": "https://lunasox.gsfc.nasa.gov"
            }
        ],
        "AdditionalMetadata": [
            {
                "Type": "SPASE",
                "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo12-LM/SWS/PT28S"
            },
            {
                "Type": "SPDF_SKT_CDF",
                "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo12_sws_28s_00000000_v01.json"
            }
        ]
    },
    {
        "Id": "APOLLO15_SWS_1HR",
        "Doi": "10.48322/70qp-jj13",
        "SpaseResourceId": "spase://NASA/NumericalData/Apollo15-LM/SWS/PT1HR",
        "Observatory": [
            "ALSEP"
        ],
        "Instrument": [
            "SWS"
        ],
        "ObservatoryGroup": [
            "Apollo"
        ],
        "InstrumentType": [
            "Particles (space)",
            "Plasma and Solar Wind"
        ],
        "Label": "Apollo 15 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
        "TimeInterval": {
            "Start": "1971-07-31T19:30:00.000Z",
            "End": "1972-06-30T17:30:00.000Z"
        },
        "PiName": "Conway W. Snyder",
        "PiAffiliation": "Jet Propulsion Laboratory ",
        "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO15_SWS_1HR",
        "DatasetLink": [
            {
                "Title": "Documentation",
                "Text": "Dataset ",
                "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
            },
            {
                "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                "Text": "Additional Data Services via",
                "Url": "https://lunasox.gsfc.nasa.gov"
            }
        ],
        "AdditionalMetadata": [
            {
              "Type": "SPASE",
              "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo15-LM/SWS/PT1HR"
            },
            {
                "Type": "SPDF_SKT_CDF",
                "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo15_sws_1hr_00000000_v01.json"
            }
        ]
    },
    {
        "Id": "APOLLO15_SWS_28S",
        "Doi": "10.48322/97e0-5h57",
        "SpaseResourceId": "spase://NASA/NumericalData/Apollo15-LM/SWS/PT28S",
        "Observatory": [
            "ALSEP"
        ],
        "Instrument": [
            "SWS"
        ],
        "ObservatoryGroup": [
            "Apollo"
        ],
        "InstrumentType": [
            "Particles (space)",
            "Plasma and Solar Wind"
        ],
        "Label": "Apollo 15 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
        "TimeInterval": {
            "Start": "1971-07-31T19:38:38.000Z",
            "End": "1972-06-30T18:14:35.000Z"
        },
        "PiName": "Conway W. Snyder",
        "PiAffiliation": "Jet Propulsion Laboratory ",
        "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO15_SWS_28S",
        "DatasetLink": [
            {
                "Title": "Documentation",
                "Text": "Dataset ",
                "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
            },
            {
                "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                "Text": "Additional Data Services via",
                "Url": "https://lunasox.gsfc.nasa.gov"
            }
        ],
        "AdditionalMetadata": [
            {
                "Type": "SPASE",
                "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo15-LM/SWS/PT28S"
            },
            {
                "Type": "SPDF_SKT_CDF",
                "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo15_sws_28s_00000000_v01.json"
            }
        ]
    }
]


APOLLO12_DATASETS = [
        {
            "Id": "APOLLO12_SWS_1HR",
            "Doi": "10.48322/vars-pj10",
            "SpaseResourceId": "spase://NASA/NumericalData/Apollo12-LM/SWS/PT1HR",
            "Observatory": [
                "ALSEP"
            ],
            "Instrument": [
                "SWS"
            ],
            "ObservatoryGroup": [
                "Apollo"
            ],
            "InstrumentType": [
                "Particles (space)",
                "Plasma and Solar Wind"
            ],
            "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
            "TimeInterval": {
                "Start": "1969-11-19T19:30:00.000Z",
                "End": "1976-03-25T08:30:00.000Z"
            },
            "PiName": "Conway W. Snyder",
            "PiAffiliation": "Jet Propulsion Laboratory ",
            "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_1HR",
            "DatasetLink": [
                {
                    "Text": "Dataset ",
                    "Title": "Documentation",
                    "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
                },
                {
                    "Text": "Additional Data Services via",
                    "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                    "Url": "https://lunasox.gsfc.nasa.gov"
                }
            ],
            "AdditionalMetadata": [
                {
                    "Type": "SPASE",
                    "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo12-LM/SWS/PT1HR"
                },
                {
                    "Type": "SPDF_SKT_CDF",
                    "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo12_sws_1hr_00000000_v01.json"
                }
            ]
        },
        {
            "Id": "APOLLO12_SWS_28S",
            "Doi": "10.48322/wh21-c403",
            "SpaseResourceId": "spase://NASA/NumericalData/Apollo12-LM/SWS/PT28S",
            "Observatory": [
                "ALSEP"
            ],
            "Instrument": [
                "SWS"
            ],
            "ObservatoryGroup": [
                "Apollo"
            ],
            "InstrumentType": [
                "Particles (space)",
                "Plasma and Solar Wind"
            ],
            "Label": "Apollo 12 Solar Wind measurements at the lunar surface - Conway W. Snyder (Jet Propulsion Laboratory )",
            "TimeInterval": {
                "Start": "1969-11-19T18:42:13.000Z",
                "End": "1976-03-25T08:35:57.000Z"
            },
            "PiName": "Conway W. Snyder",
            "PiAffiliation": "Jet Propulsion Laboratory ",
            "Notes": "https://cdaweb.gsfc.nasa.gov/misc/NotesA.html#APOLLO12_SWS_28S",
            "DatasetLink": [
                {
                    "Text": "Dataset ",
                    "Title": "Documentation",
                    "Url": "https://nssdc.gsfc.nasa.gov/nmc/publicationDisplay.do?id=B55381-000A"
                },
                {
                    "Text": "Additional Data Services via",
                    "Title": " the Lunar Surface Origins Exploration service (LUNASOX)",
                    "Url": "https://lunasox.gsfc.nasa.gov"
                }
            ],
            "AdditionalMetadata": [
                {
                    "Type": "SPASE",
                    "value": "https://heliophysicsdata.gsfc.nasa.gov/WS/hdp/1/Spase?ResourceID=spase://NASA/NumericalData/Apollo12-LM/SWS/PT28S"
                },
                {
                    "Type": "SPDF_SKT_CDF",
                    "value": "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0JSONS/apollo12_sws_28s_00000000_v01.json"
                }
            ]
        }
    ]


AC_INSTRUMENT_TYPES = [
        {
            "Name": "Ephemeris/Attitude/Ancillary"
        },
        {
            "Name": "Magnetic Fields (space)"
        },
        {
            "Name": "Particles (space)"
        },
        {
            "Name": "Plasma and Solar Wind"
        }
    ]

ALSEP_INSTRUMENTS = [
        {
            "LongDescription": "Solar Wind Spectrometer",
            "Name": "SWS",
            "ShortDescription": "Solar Wind Spectrometer"
        }
    ]

ALSEP_OBSERVATORY = [
        {
            "LongDescription": "Apollo Lunar Surface Experiment Package",
            "Name": "ALSEP",
            "ShortDescription": "Apollo Lunar Surface Experiment Package"
        }
    ]

BALLOON_INSTRUMENTS = [
        {
            "Name": "Balloons",
            "ObservatoryInstruments": [
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1B"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1C"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1D"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1G"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1H"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1I"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1J"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1K"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1M"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1N"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1O"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1Q"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1R"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1S"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1T"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1U"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_1V"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2B"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2C"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2D"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2E"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2F"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2I"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2K"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2L"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2M"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2N"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2O"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2P"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2Q"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2T"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2W"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2X"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_2Y"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3B"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3C"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3D"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3E"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3F"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_3G"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_6A"
                },
                {
                    "InstrumentDescription": [
                        {
                            "LongDescription": "Magnetometer",
                            "Name": "MAGN",
                            "ShortDescription": "Magnetometer"
                        }
                    ],
                    "Name": "bar_7A"
                }
            ]
        }
    ]

MMS1_FPI_BRST_INVENTORY = [
    TimeInterval("2018-08-30T08:09:53.000Z", "2018-08-30T08:13:12.000Z"),
    TimeInterval("2018-08-30T08:39:23.000Z", "2018-08-30T08:44:02.000Z"),
    TimeInterval("2018-08-30T08:50:43.000Z", "2018-08-30T08:55:02.000Z")
]


AC_H2_MFI_VARIABLES = [
        {
            "LongDescription": "B-field magnitude",
            "Name": "Magnitude",
            "ShortDescription": "magnetic_field>magnitude"
        },
        {
            "LongDescription": "Magnetic Field Vector in GSE Cartesian coordinates (1 hr)",
            "Name": "BGSEc",
            "ShortDescription": "magnetic_field"
        },
        {
            "LongDescription": "Magnetic field vector in GSM coordinates (1 hr)",
            "Name": "BGSM",
            "ShortDescription": ""
        },
        {
            "LongDescription": "ACE s/c position, 3 comp. in GSE coord.",
            "Name": "SC_pos_GSE",
            "ShortDescription": "position>gse_cartesian"
        },
        {
            "LongDescription": "ACE s/c position, 3 comp. in GSM coord.",
            "Name": "SC_pos_GSM",
            "ShortDescription": "position>gsm_cartesian"
        }
    ]

AC_H1_MFI_DATA_FILE_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T11:08:37.000Z",
            "Length": 42506,
            "MimeType": "application/x-cdf",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/ac_h1s_mfi_20090601000000_20090601000800_cdaweb.cdf",
            "StartTime": "2009-06-01T00:00:00.000Z"
        }
    ]
}

AC_H1_MFI_GRAPH_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T11:08:37.000Z",
            "Length": 42506,
            "MimeType": "application/pdf",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsgq5wcm/AC_H1_MFI__000.pdf",
            "StartTime": "2009-06-01T00:00:00.000Z"
        }
    ]
}

IM_K0_EUV_GRAPH_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2005-01-02T00:00:00.000Z",
            "LastModified": "2019-06-06T14:57:13.000Z",
            "Length": 128469,
            "MimeType": "image/png",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsNiq0jr/IM_K0_EUV__000.png",
            "StartTime": "2005-01-01T00:00:00.000Z",
            "ThumbnailDescription": {
                "Dataset": "IM_K0_EUV",
                "MyScale": 0.0,
                "Name": "wsNiq0jr/IM_K0_EUV__000.png",
                "NumCols": 10,
                "NumFrames": 76,
                "NumRows": 8,
                "Options": 0,
                "StartRecord": 0,
                "ThumbnailHeight": 62,
                "ThumbnailWidth": 50,
                "TimeInterval": {
                    "End": "2005-01-02T00:00:00.000Z",
                    "Start": "2005-01-01T00:00:00.000Z"
                },
                "TitleHeight": 10,
                "VarName": "IMAGE",
                "XyStep": 0.0
            },
            "ThumbnailId": "-1eacebf9:16a6e475b99:-5635"
        }
    ]
}

IM_K0_EUV_THUMBNAIL_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2005-01-02T00:00:00.000Z",
            "LastModified": "2019-06-06T14:57:13.000Z",
            "Length": 37851,
            "MimeType": "image/png",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsNiq0jr/IM_K0_EUV__000_f038.png",
            "StartTime": "2005-01-01T00:00:00.000Z"
        }
    ]
}

AC_H1_MFI_TEXT_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T14:57:14.000Z",
            "Length": 4529,
            "MimeType": "text/plain",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/ws2zybtw/ac_h1_mfi.txt",
            "StartTime": "2009-06-01T00:00:00.000Z"
        }
    ]
}

AC_H1_MFI_AUDIO_RESULT = {
    "FileDescription": [
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T14:57:14.000Z",
            "Length": 52,
            "MimeType": "audio/wav",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsSS3EqN/AC_H1_MFI__000_000.wav",
            "StartTime": "2009-06-01T00:00:00.000Z"
        },
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T14:57:14.000Z",
            "Length": 52,
            "MimeType": "audio/wav",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsSS3EqN/AC_H1_MFI__001_000.wav",
            "StartTime": "2009-06-01T00:00:00.000Z"
        },
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T14:57:14.000Z",
            "Length": 52,
            "MimeType": "audio/wav",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsSS3EqN/AC_H1_MFI__001_001.wav",
            "StartTime": "2009-06-01T00:00:00.000Z"
        },
        {
            "EndTime": "2009-06-01T00:10:00.000Z",
            "LastModified": "2019-06-06T14:57:14.000Z",
            "Length": 52,
            "MimeType": "audio/wav",
            "Name": "https://cdaweb.gsfc.nasa.gov/tmp/wsSS3EqN/AC_H1_MFI__001_002.wav",
            "StartTime": "2009-06-01T00:00:00.000Z"
        }
    ]
}


# pylint: enable=line-too-long


# Variable portion of url path regex.  Can this be enhanced to ignore the
# hostname/port and http/https to support testing with http://cdaweb-dev...?
VARIABLE_URL_PATH = re.compile(r'/ws.+/')


class TestCdasWs(unittest.TestCase):
    """
    Class for unittest of CdasWs class.
    """

    def __init__(self, *args, **kwargs):
        super(TestCdasWs, self).__init__(*args, **kwargs)
        self.maxDiff = None
        self._cdas = CdasWs()


    #@unittest.skip("Skip until BALLOONS is restored in cdaweb")
    def test_get_observatory_groups(self):
        """
        Test of get_observatory_group method.
        """

        self.assertListEqual(
            self._cdas.get_observatory_groups(
                instrumentType='Magnetic Fields (Balloon)'),
            BALLOONS_OBSERV_GROUP)


    def test_get_instrument_types(self):
        """
        Test of get_instrument_types method.
        """

        self.assertListEqual(
            self._cdas.get_instrument_types(observatory='AC'),
            AC_INSTRUMENT_TYPES)


    def test_get_instruments(self):
        """
        Test of get_instruments method.
        """

        self.assertListEqual(
            self._cdas.get_instruments(observatory='ALSEP'),
            ALSEP_INSTRUMENTS)


    def test_get_observatories(self):
        """
        Test of get_observatories method.
        """

        self.assertListEqual(
            self._cdas.get_observatories(instrument='SWS'),
            ALSEP_OBSERVATORY)


    #@unittest.skip("Skip until BARREL is restored in cdaweb")
    def test_get_observatory_groups_and_instruments(self):
        """
        Test of get_observatory_groups_and_instruments method.
        """

        #groups_instr = self._cdas.get_observatory_groups_and_instruments(
        #                   instrumentType='Magnetic Fields (Balloon)')
        #print(json.dumps(groups_instr, indent=4))
        self.assertListEqual(
            self._cdas.get_observatory_groups_and_instruments(
                instrumentType='Magnetic Fields (Balloon)'),
            BALLOON_INSTRUMENTS)


    def test_get_datasets(self):
        """
        Test of get_datasets method.
        """

        self.assertListEqual(
            self._cdas.get_datasets(observatoryGroup=['Apollo'],
                                    instrumentType='Plasma and Solar Wind'), 
            APOLLO_SWP_DATASETS)

        self.assertListEqual(
            self._cdas.get_datasets(idPattern='APOLLO12.*'),
            APOLLO12_DATASETS)

        self.assertListEqual(
            self._cdas.get_datasets(id='10.48322/vars-pj10'),
            APOLLO12_SWS_1HR_DATASETS)

        self.assertListEqual(
            self._cdas.get_datasets(id='spase://NASA/NumericalData/Apollo12-LM/SWS/PT1HR'),
            APOLLO12_SWS_1HR_DATASETS)


    def test_get_inventory(self):
        """
        Test of get_inventory method.
        """

        self.assertListEqual(
            self._cdas.get_inventory(
                'MMS1_FPI_BRST_L2_DES-MOMS',
                timeInterval=TimeInterval('2018-08-30T08:09:53Z',
                                          '2018-08-30T08:52:00Z')),
            MMS1_FPI_BRST_INVENTORY)


    def test_get_variables(self):
        """
        Test of get_variables method.
        """

        self.assertListEqual(
            self._cdas.get_variables('AC_H2_MFI'),
            AC_H2_MFI_VARIABLES)


    def test_get_ssc_id(self):
        """
        Test of get_ssc_id method.
        """

        self.assertListEqual(
            self._cdas.get_ssc_id('TWINS_M2_ENA')[1],
            ['twins2', 'twins1'])

        self.assertEqual(
            self._cdas.get_ssc_id('MMS1_FPI_BRST_L2_DES-MOMS')[1],
            'mms1')


    def test_get_data_exception(self):
        """
        Test of get_data method exception.
        """

        with self.assertRaises(ValueError):
            self._cdas.get_data('dummy_ds', ['dummy_var'],
                                'bad_datetime', 'bad_datetime')

        with self.assertRaises(ValueError):
            self._cdas.get_data('dummy_ds', ['dummy_var'],
                                datetime.now(), 123)

        with self.assertRaises(ValueError):
            self._cdas.get_data('dummy_ds', ['dummy_var'],
                                123)


    def test_get_data(self):
        """
        Test of get_data method.
        """

        status, data = \
            self._cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                '2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z'
                               )

        self.assertEqual(status['http']['status_code'], 200)
        #self.assertEqual(data, ???)

        time_intervals = [
            TimeInterval('2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z'),
            TimeInterval('2009-06-02T00:00:00Z', '2009-06-02T00:10:00Z')
        ]
        status, data = \
            self._cdas.get_data('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                time_intervals
                               )

        self.assertEqual(status['http']['status_code'], 200)
        #self.assertEqual(data, ???)


    @staticmethod
    def equivalent_dataresults(value1: Dict, value2: Dict) -> bool:
        """
        Compares the given dictionary representations of DataResult
        objects from
        <https://cdaweb.gsfc.nasa.gov/WebServices/REST/CDAS.xsd>.
        The two values are equivalent if they only differ by the
        randomly generated portion of the FileDescription/Name and
        FileDescription/LastModified.

        Parameters
        ----------
        value1
            First DataResult dictionary representation.
        value2
            Second DataResult dictionary representation.
        Returns
        -------
        bool
            True if the two values only differ by the randomly
            generated portion of the FileDescription/Name and
            FileDescription/LastModified.  Otherwise
            false.
        """

        values = [value1.get('FileDescription', None),
                  value2.get('FileDescription', None)]

        if values[0] is not None and values[1] is not None and \
           len(values[0]) == len(values[1]):

            for file1, file2 in zip(values[0], values[1]):
                for key in file1:
                    # use special code below to check Name
                    # LastModified and ThumbnailId will always 
                    #   be different
                    # Length varies a little for png files
                    if key != 'Name' and key != 'LastModified' and \
                       key != 'ThumbnailDescription' and \
                       key != 'ThumbnailId' and key != 'Length' and \
                       file1[key] != file2[key]:
                        print('bad key value', key, file1[key], file2[key])
                        return False

                if re.sub(VARIABLE_URL_PATH, '/', file1['Name']) != \
                   re.sub(VARIABLE_URL_PATH, '/', file2['Name']):

                    print('bad Name ',
                          re.sub(VARIABLE_URL_PATH, '/', file1['Name']),
                          re.sub(VARIABLE_URL_PATH, '/', file2['Name']))
                    return False
            return True

        print('bad values', len(values[0]), len(values[1]))
        print(value1)
        print(value2)
        return False


    def test_get_data_file(self):
        """
        Test of get_data_file method.
        """

        status, result = \
            self._cdas.get_data_file('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                     '2009-06-01T00:00:00Z',
                                     '2009-06-01T00:10:00Z'
                                    )
        self.assertEqual(status, 200)
        self.assertTrue(
            TestCdasWs.equivalent_dataresults(result,
                                              AC_H1_MFI_DATA_FILE_RESULT))

    def test_get_graph(self):
        """
        Test of get_graph method.
        """

        status, result = \
            self._cdas.get_graph('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                 '2009-06-01T00:00:00Z',
                                 '2009-06-01T00:10:00Z',
                                 GraphOptions(coarse_noise_filter=True,
                                              y_axis_height_factor=2,
                                              combine=True,
                                              overplot=Overplot.VECTOR_COMPONENTS),
                                 [ImageFormat.PDF]
                                 )
        self.assertEqual(status, 200)
        self.assertTrue(
            TestCdasWs.equivalent_dataresults(result,
                                              AC_H1_MFI_GRAPH_RESULT))

    def test_get_graph_thumbnail(self):
        """
        Test of get_graph (thumbnail) method.
        """

        status, result = \
            self._cdas.get_graph('IM_K0_EUV', ['IMAGE'],
                                 '2005-01-01T00:00:00Z',
                                 '2005-01-02T00:00:00Z')

        self.assertEqual(status, 200)
        self.assertTrue(
            TestCdasWs.equivalent_dataresults(result,
                                              IM_K0_EUV_GRAPH_RESULT))

        thumbnail_id = result['FileDescription'][0].get('ThumbnailId', None)
        if thumbnail_id is not None:
            thumbnail = result['FileDescription'][0]['ThumbnailDescription']['NumFrames'] // 2
            status, result = \
                self._cdas.get_thumbnail('IM_K0_EUV', ['IMAGE'],
                                         '2005-01-01T00:00:00Z',
                                         '2005-01-02T00:00:00Z',
                                         thumbnail_id, thumbnail)
            self.assertEqual(status, 200)
            self.assertTrue(
                TestCdasWs.equivalent_dataresults(result,
                                                  IM_K0_EUV_THUMBNAIL_RESULT))


    def test_get_audio(self):
        """
        Test of get_audio method.
        """

        status, result = \
            self._cdas.get_audio('AC_H1_MFI', ['Magnitude', 'BGSEc'],
                                 '2009-06-01T00:00:00Z',
                                 '2009-06-01T00:10:00Z',
                                 )
        self.assertEqual(status, 200)
        self.assertTrue(
            TestCdasWs.equivalent_dataresults(result,
                                              AC_H1_MFI_AUDIO_RESULT))


    def test_get_doi_landing_page_url(self):
        """
        Test of get_doi_landing_page_url method.
        """

        doi = '10.48322/e0dc-0h53'
        result = \
            self._cdas.get_doi_landing_page_url(doi)
        self.assertEqual(result, 'https://doi.org/' + doi)


    def test_get_citation(self):
        """
        Test of get_citation method.
        """

        doi = '10.48322/541v-1f57'
        result = \
            self._cdas.get_citation(doi)
        self.assertEqual(result, 'Nakamura, R., Torkar, K. M., Jeszenszky, H., &amp; Burch, J. L. (2022). <i>MMS 1 Active Spacecraft Potential Control (ASPOC), Sensors 1 and 2, Level 2 (L2), Survey Mode, 1 s Data</i> [Data set]. NASA Space Physics Data Facility. https://doi.org/10.48322/541V-1F57')


if __name__ == '__main__':
    unittest.main()
