#!/usr/bin/env python

# Copyright (C) 2006-2016  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/



from essentia_test import *


class TestDanceability(TestCase):
    def testEmpty(self):
        d, dfa = Danceability()([])
        self.assertEqual(d, 0)
        self.assertEqualVector(dfa, [0.] * 36)

    def testOne(self):
        d, dfa = Danceability()([10])
        self.assertEqual(d, 0)
        self.assertEqualVector(dfa, [0.] * 36)

    def testSilence(self):
        d, dfa = Danceability()([0]*44100)
        self.assertEqual(d, 0)
        self.assertEqualVector(dfa, [0.] * 36)

        d, dfa = Danceability()([0]*100000)
        self.assertEqual(d, 0)
        self.assertEqualVector(dfa, [0.] * 36)

    def testRegression(self):
        audio = MonoLoader(filename = join(testdata.audio_dir, 'recorded', 'techno_loop.wav'),
                            downmix='left', sampleRate=44100)()
        d, dfa = Danceability()(audio)
        dfa_expected = [8.24911475e-01, 7.70361125e-01, 7.48310685e-01, 7.43584096e-01,
                        7.18539476e-01, 6.26609206e-01, 4.46862280e-01, 2.66744852e-01,
                        1.67193800e-01, 1.42737418e-01, 1.68398589e-01, 2.68227428e-01,
                        3.35482270e-01, 2.54870266e-01, 1.76126286e-01, 1.69479221e-01,
                        2.44752705e-01, 2.25030452e-01, 2.16719568e-01, 2.74833381e-01,
                        2.14674041e-01, 1.73826352e-01, 1.41980320e-01, 1.62845716e-01,
                        1.35091081e-01, 1.59601390e-01, 1.93217084e-01, 1.67348266e-01,
                        7.95856640e-02, 4.29583378e-02, 8.19148670e-04, -4.16366570e-02,
                        1.58639736e-02, 3.06910593e-02, 3.92476730e-02, 0.00000000e+00]

        self.assertAlmostEqual(d, 3.76105952263, 5e-3)
        self.assertAlmostEqualVector(dfa, dfa_expected, 5e-3)

    def testSanity(self):
        filename = join(testdata.audio_dir, 'recorded', 'spaceambient.wav')
        ambientAudio = MonoLoader(filename=filename,
                                 downmix='left',
                                 sampleRate=44100)()
        filename = join(testdata.audio_dir, 'recorded', 'techno_loop.wav')
        technoAudio = MonoLoader(filename=filename,
                                  downmix='left',
                                  sampleRate=44100)()

        ambientDanceability = Danceability()(ambientAudio)
        technoDanceability = Danceability()(technoAudio)

        self.assertTrue(ambientDanceability < technoDanceability)

    def testMinBiggerThanMaxTau(self):
        self.assertConfigureFails(Danceability(), {'minTau':1000, 'maxTau':500})


    def testWhiteNoise(self):
        # 5 seconds of white noise
        wn_44100 = np.random.randn(44100 * 5)
        print Danceability()(wn_44100)


suite = allTests(TestDanceability)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
