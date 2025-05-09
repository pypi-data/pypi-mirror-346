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
# Copyright (c) 2019-2025 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the CdasWs class.<br>

Copyright &copy; 2019-2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import unittest
#from datetime import datetime, timezone

from context import cdasws  # pylint: disable=unused-import

# pylint: disable=import-error
from cdasws.timeinterval import TimeInterval
from cdasws.datarequest import CdfRequest, TextRequest
from cdasws.datarequest import GraphRequest, GraphOptions, Overplot
from cdasws.datarequest import ImageFormat, ThumbnailRequest, AudioRequest
from cdasws.datarequest import Compression, TextFormat
# pylint: enable=import-error


# pylint: disable=line-too-long

CDF_REQUEST = '{\
"CdfRequest": {\
"BinData": {\
"InterpolateMissingValues": true, \
"Interval": 60.0, \
"OverrideDefaultBinning": false, \
"SigmaMultiplier": 4\
}, \
"CdfFormat": "Binary", \
"CdfVersion": 3, \
"DatasetRequest": {\
"DatasetId": "AC_H1_MFI", \
"VariableName": [\
"Magnitude", \
"BGSEc"\
]\
}, \
"TimeInterval": [{\
"End": "2009-06-01T00:10:00+00:00", \
"Start": "2009-06-01T00:00:00+00:00"\
}, {\
"End": "2009-07-01T00:10:00+00:00", \
"Start": "2009-07-01T00:00:00+00:00"\
}\
]\
}\
}'

#CDF_XML_REQUEST = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\
CDF_XML_REQUEST = b'<DataRequest xmlns="http://cdaweb.gsfc.nasa.gov/schema">\
<CdfRequest>\
<TimeInterval>\
<Start>2009-06-01T00:00:00Z</Start>\
<End>2009-06-01T00:10:00Z</End>\
</TimeInterval>\
<TimeInterval>\
<Start>2009-07-01T00:00:00Z</Start>\
<End>2009-07-01T00:10:00Z</End>\
</TimeInterval>\
<DatasetRequest>\
<DatasetId>AC_H1_MFI</DatasetId>\
<VariableName>Magnitude</VariableName>\
<VariableName>BGSEc</VariableName>\
</DatasetRequest>\
<CdfVersion>3</CdfVersion>\
<CdfFormat>Binary</CdfFormat>\
<BinData>\
<Interval>60.0</Interval>\
<InterpolateMissingValues>true</InterpolateMissingValues>\
<SigmaMultiplier>4</SigmaMultiplier>\
<OverrideDefaultBinning>false</OverrideDefaultBinning>\
</BinData>\
</CdfRequest>\
</DataRequest>'


TEXT_REQUEST = '{"TextRequest": {"BinData": {"InterpolateMissingValues": true, "Interval": 60.0, "OverrideDefaultBinning": false, "SigmaMultiplier": 4}, "Compression": "Uncompressed", "DatasetRequest": {"DatasetId": "AC_H1_MFI", "VariableName": ["Magnitude", "BGSEc"]}, "Format": "Plain", "TimeInterval": {"End": "2009-06-01T00:10:00+00:00", "Start": "2009-06-01T00:00:00+00:00"}}}'

TEXT_XML_REQUEST = b'<DataRequest xmlns="http://cdaweb.gsfc.nasa.gov/schema">\
<TextRequest>\
<TimeInterval>\
<Start>2009-06-01T00:00:00Z</Start>\
<End>2009-06-01T00:10:00Z</End>\
</TimeInterval>\
<DatasetRequest>\
<DatasetId>AC_H1_MFI</DatasetId>\
<VariableName>Magnitude</VariableName>\
<VariableName>BGSEc</VariableName>\
</DatasetRequest>\
<Compression>Uncompressed</Compression>\
<Format>Plain</Format>\
<BinData>\
<Interval>60.0</Interval>\
<InterpolateMissingValues>true</InterpolateMissingValues>\
<SigmaMultiplier>4</SigmaMultiplier>\
<OverrideDefaultBinning>false</OverrideDefaultBinning>\
</BinData>\
</TextRequest>\
</DataRequest>'


GRAPH_REQUEST = '{"GraphRequest": {"BinData": {"InterpolateMissingValues": true, "Interval": 60.0, "OverrideDefaultBinning": false, "SigmaMultiplier": 4}, "DatasetRequest": {"DatasetId": "AC_H1_MFI", "VariableName": ["Magnitude", "BGSEc"]}, "GraphOptions": {"Overplot": "None", "XAxisWidthFactor": 1, "YAxisHeightFactor": 1}, "ImageFormat": ["PNG"], "TimeInterval": {"End": "2009-06-01T00:10:00+00:00", "Start": "2009-06-01T00:00:00+00:00"}}}'

GRAPH_XML_REQUEST = b'<DataRequest xmlns="http://cdaweb.gsfc.nasa.gov/schema">\
<GraphRequest>\
<TimeInterval>\
<Start>2009-06-01T00:00:00Z</Start>\
<End>2009-06-01T00:10:00Z</End>\
</TimeInterval>\
<DatasetRequest>\
<DatasetId>AC_H1_MFI</DatasetId>\
<VariableName>Magnitude</VariableName>\
<VariableName>BGSEc</VariableName>\
</DatasetRequest>\
<GraphOptions>\
<XAxisWidthFactor>1</XAxisWidthFactor>\
<YAxisHeightFactor>1</YAxisHeightFactor>\
<Overplot>None</Overplot>\
</GraphOptions>\
<ImageFormat>PNG</ImageFormat>\
<BinData>\
<Interval>60.0</Interval>\
<InterpolateMissingValues>true</InterpolateMissingValues>\
<SigmaMultiplier>4</SigmaMultiplier>\
<OverrideDefaultBinning>false</OverrideDefaultBinning>\
</BinData>\
</GraphRequest>\
</DataRequest>'


THUMBNAIL_REQUEST = '{"ThumbnailRequest": {"DatasetRequest": {"DatasetId": "AC_H1_MFI", "VariableName": ["Magnitude", "BGSEc"]}, "ImageFormat": ["GIF", "PDF"], "Thumbnail": 2, "ThumbnailId": "dummy-thumbnail-identifier", "TimeInterval": {"End": "2009-06-01T00:10:00+00:00", "Start": "2009-06-01T00:00:00+00:00"}}}'

THUMBNAIL_XML_REQUEST = b'<DataRequest xmlns="http://cdaweb.gsfc.nasa.gov/schema">\
<ThumbnailRequest>\
<TimeInterval>\
<Start>2009-06-01T00:00:00Z</Start>\
<End>2009-06-01T00:10:00Z</End>\
</TimeInterval>\
<DatasetRequest>\
<DatasetId>AC_H1_MFI</DatasetId>\
<VariableName>Magnitude</VariableName>\
<VariableName>BGSEc</VariableName>\
</DatasetRequest>\
<Thumbnail>2</Thumbnail>\
<ThumbnailId>dummy-thumbnail-identifier</ThumbnailId>\
<ImageFormat>GIF</ImageFormat>\
<ImageFormat>PDF</ImageFormat>\
</ThumbnailRequest>\
</DataRequest>'


AUDIO_REQUEST = '{"AudioRequest": {"BinData": {"InterpolateMissingValues": true, "Interval": 60.0, "OverrideDefaultBinning": false, "SigmaMultiplier": 4}, "DatasetRequest": {"DatasetId": "AC_H1_MFI", "VariableName": ["Magnitude", "BGSEc"]}, "TimeInterval": {"End": "2009-06-01T00:10:00+00:00", "Start": "2009-06-01T00:00:00+00:00"}}}'

AUDIO_XML_REQUEST = b'<DataRequest xmlns="http://cdaweb.gsfc.nasa.gov/schema">\
<AudioRequest>\
<TimeInterval>\
<Start>2009-06-01T00:00:00Z</Start>\
<End>2009-06-01T00:10:00Z</End>\
</TimeInterval>\
<DatasetRequest>\
<DatasetId>AC_H1_MFI</DatasetId>\
<VariableName>Magnitude</VariableName>\
<VariableName>BGSEc</VariableName>\
</DatasetRequest>\
<BinData>\
<Interval>60.0</Interval>\
<InterpolateMissingValues>true</InterpolateMissingValues>\
<SigmaMultiplier>4</SigmaMultiplier>\
<OverrideDefaultBinning>false</OverrideDefaultBinning>\
</BinData>\
</AudioRequest>\
</DataRequest>'


# pylint: enable=line-too-long


class TestDataRequest(unittest.TestCase):
    """
    Class for unittest of DataRequest class.
    """

    def __init__(self, *args, **kwargs):
        super(TestDataRequest, self).__init__(*args, **kwargs)
        self.maxDiff = None # pylint: disable=invalid-name


    def test_cdfrequest_init(self):
        """
        Test for CdfRequest constructor.
        """

        intervals = [
            TimeInterval('2009-06-01T00:00:00Z', '2009-06-01T00:10:00Z'),
            TimeInterval('2009-07-01T00:00:00Z', '2009-07-01T00:10:00Z')
        ]
        request = CdfRequest('AC_H1_MFI',
                             ['Magnitude', 'BGSEc'],
                             intervals,
                             #3, CdfFormat.BINARY,
                             binData={
                                 'interval': 60.0,
                                 'interpolateMissingValues': True,
                                 'sigmaMultiplier': 4,
                                 'overrideDefaultBinning': False
                             }
                             )

        self.assertEqual(request.json(sort_keys=True), CDF_REQUEST)
        self.assertEqual(request.xml_str(), CDF_XML_REQUEST)


    def test_textrequest_init(self):
        """
        Test for TextRequest constructor.
        """

        request = TextRequest('AC_H1_MFI',
                              ['Magnitude', 'BGSEc'],
                              TimeInterval('2009-06-01T00:00:00Z',
                                           '2009-06-01T00:10:00Z'),
                              Compression.UNCOMPRESSED, TextFormat.PLAIN,
                               binData={
                                   'interval': 60.0,
                                   'interpolateMissingValues': True,
                                   'sigmaMultiplier': 4,
                                   'overrideDefaultBinning': False
                               }
                             )

        self.assertEqual(request.json(sort_keys=True), TEXT_REQUEST)
        self.assertEqual(request.xml_str(), TEXT_XML_REQUEST)


    def test_graphoptions_properties(self):
        """
        Test for GraphOptions properties.
        """

        options = GraphOptions(False, 1, False, Overplot.NONE)

        options.coarse_noise_filter = True
        options.y_axis_height_factor = 2
        options.combine = True
        options.overplot = Overplot.VECTOR_COMPONENTS

        self.assertEqual(options.coarse_noise_filter, True)
        self.assertEqual(options.y_axis_height_factor, 2)
        self.assertEqual(options.combine, True)
        self.assertEqual(options.overplot, Overplot.VECTOR_COMPONENTS)


    def test_graphrequest_init(self):
        """
        Test for GraphRequest constructor.
        """

        request = GraphRequest('AC_H1_MFI',
                               ['Magnitude', 'BGSEc'],
                               TimeInterval('2009-06-01T00:00:00Z',
                                            '2009-06-01T00:10:00Z'),
                               GraphOptions(False, 1, 1, False, Overplot.NONE),
                               binData={
                                   'interval': 60.0,
                                   'interpolateMissingValues': True,
                                   'sigmaMultiplier': 4,
                                   'overrideDefaultBinning': False
                               }
                              )

        self.assertEqual(request.json(sort_keys=True), GRAPH_REQUEST)
        self.assertEqual(request.xml_str(), GRAPH_XML_REQUEST)


    def test_thumbnailrequest_init(self):
        """
        Test for ThumbnailRequest constructor.
        """
        request = ThumbnailRequest('AC_H1_MFI',
                                   ['Magnitude', 'BGSEc'],
                                   TimeInterval('2009-06-01T00:00:00Z',
                                                '2009-06-01T00:10:00Z'),
                                   "dummy-thumbnail-identifier",
                                   2,
                                   [ImageFormat.GIF, ImageFormat.PDF]
                                  )

        self.assertEqual(request.json(sort_keys=True), THUMBNAIL_REQUEST)
        self.assertEqual(request.xml_str(), THUMBNAIL_XML_REQUEST)


    def test_audiorequest_init(self):
        """
        Test for AudioRequest constructor.
        """
        request = AudioRequest('AC_H1_MFI',
                               ['Magnitude', 'BGSEc'],
                               TimeInterval('2009-06-01T00:00:00Z',
                                            '2009-06-01T00:10:00Z'),
                               binData={
                                   'interval': 60.0,
                                   'interpolateMissingValues': True,
                                   'sigmaMultiplier': 4,
                                   'overrideDefaultBinning': False
                               }
                              )

        self.assertEqual(request.json(sort_keys=True), AUDIO_REQUEST)
        self.assertEqual(request.xml_str(), AUDIO_XML_REQUEST)



if __name__ == '__main__':
    unittest.main()
