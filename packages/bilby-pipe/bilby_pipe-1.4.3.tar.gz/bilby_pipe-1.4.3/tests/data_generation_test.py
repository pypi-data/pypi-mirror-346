import os
import shutil
import unittest

import gwpy
import mock

import bilby
from bilby_pipe.data_generation import DataGenerationInput, create_generation_parser
from bilby_pipe.main import parse_args
from bilby_pipe.utils import BilbyPipeError, DataDump


class TestDataGenerationInput(unittest.TestCase):
    def setUp(self):
        self.outdir = "test_outdir"
        self.default_args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            "--outdir",
            self.outdir,
            "--data-label",
            "TEST",
        ]
        self.parser = create_generation_parser()
        self.inputs = DataGenerationInput(
            *parse_args(self.default_args_list, self.parser), create_data=False
        )
        self.gps_file = "tests/gps_file.txt"

    def tearDown(self):
        del self.default_args_list
        del self.parser
        del self.inputs
        if os.path.isdir(self.outdir):
            shutil.rmtree(self.outdir)

    def test_cluster_set(self):
        self.inputs.cluster = 123
        self.assertEqual(123, self.inputs.cluster)

    def test_process_set(self):
        self.inputs.process = 321
        self.assertEqual(321, self.inputs.process)

    def test_parameter_conversion(self):
        self.inputs.frequency_domain_source_model = "binary_neutron_star"
        self.assertEqual(
            self.inputs.parameter_conversion,
            bilby.gw.conversion.convert_to_lal_binary_neutron_star_parameters,
        )
        self.inputs.frequency_domain_source_model = "binary_black_hole"
        self.assertEqual(
            self.inputs.parameter_conversion,
            bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters,
        )

    def test_psd_length_set(self):
        self.inputs.psd_length = 10
        self.assertEqual(10, self.inputs.psd_length)
        self.assertEqual(
            10 * self.inputs.duration, self.inputs.psd_length * self.inputs.duration
        )

    def test_psd_length(self):
        self.inputs.duration = 4
        self.inputs.psd_length = 32
        self.assertEqual(32, self.inputs.psd_length)
        self.assertEqual(4, self.inputs.duration)
        self.assertEqual(
            self.inputs.psd_length * self.inputs.duration, self.inputs.psd_duration
        )

    def test_psd_length_over_maximum(self):
        self.inputs.duration = 128
        self.inputs.psd_length = 32
        self.assertEqual(32, self.inputs.psd_length)
        self.assertEqual(128, self.inputs.duration)
        self.assertEqual(1024, self.inputs.psd_duration)

    def test_psd_length_over_custom_maximum(self):
        self.inputs.psd_maximum_duration = 2048
        self.inputs.duration = 128
        self.inputs.psd_length = 32
        self.assertEqual(32, self.inputs.psd_length)
        self.assertEqual(128, self.inputs.duration)
        self.assertEqual(2048, self.inputs.psd_duration)

    def test_psd_dict(self):
        self.inputs.psd_dict = "{H1:tests/DATA/psd.txt, L1:tests/DATA/psd.txt}"
        self.assertEqual(self.inputs.psd_dict["H1"], "tests/DATA/psd.txt")

    def test_set_reference_frequency(self):
        args_list = self.default_args_list + ["--reference-frequency", "10"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.reference_frequency, 10)

    def test_psd_length_default(self):
        self.assertEqual(32 * self.inputs.duration, self.inputs.psd_duration)

    def test_psd_start_time_set(self):
        self.inputs.psd_start_time = 10
        self.assertEqual(10, self.inputs.psd_start_time)

    def test_psd_start_time_default(self):
        self.inputs.psd_duration = 4
        self.inputs.trigger_time = 12
        self.assertEqual(-4, self.inputs.psd_start_time)

    # def test_psd_start_time_fail(self):
    #    self.inputs.psd_duration = 4
    #    self.inputs.duration = 4
    #    self.inputs.trigger_time = 2
    #    self.inputs.start_time = 0
    #    self.inputs.psd_start_time = None
    #    with self.assertRaises(BilbyPipeError):
    #        self.assertEqual(10 - 4, self.inputs.psd_start_time)

    def test_script_inputs_from_test_ini(self):
        self.assertEqual(
            self.inputs.channel_dict, dict(H1="GDS-CALIB_STRAIN", L1="GDS-CALIB_STRAIN")
        )
        self.assertEqual(self.inputs.label, "label")

    def test_interferometer_unset(self):
        with self.assertRaises(ValueError):
            self.inputs.interferometers

    def test_interferometer_set(self):
        ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])
        self.inputs.interferometers = ifos
        self.assertEqual(ifos, self.inputs.interferometers)

    def test_script_inputs_detectors_from_ini(self):
        self.assertEqual(self.inputs.detectors, ["H1", "L1"])

    def test_script_inputs_detectors_from_command_line(self):
        args_list = self.default_args_list + ["--detectors", "H1", "--detectors", "L1"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

        args_list = self.default_args_list + ["--detectors", "H1 L1"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

        args_list = self.default_args_list + ["--detectors", "L1 H1"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

        args_list = self.default_args_list + ["--detectors", "[L1, H1]"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )

        args_list = self.default_args_list + ["--detectors", "[L1 H1]"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

        args_list = self.default_args_list + ["--detectors", '["L1", "H1"]']
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

        args_list = self.default_args_list + ["--detectors", "['L1', 'H1']"]
        inputs = DataGenerationInput(
            *parse_args(args_list, self.parser), create_data=False
        )
        self.assertEqual(inputs.detectors, ["H1", "L1"])

    def test_detectors_not_understood(self):
        with self.assertRaises(BilbyPipeError):
            self.inputs.detectors = 10

    # def test_trigger_time(self):
    #    args_list = [
    #        "--ini",
    #        "tests/test_data_generation.ini",
    #        "--outdir",
    #        self.outdir,
    #        "--trigger-time",
    #        "1126259462",
    #        "--data-label",
    #        "TEST",
    #    ]
    #    self.inputs = DataGenerationInput(*parse_args(args_list, self.parser))

    def test_injections_no_file(self):
        args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            "--outdir",
            self.outdir,
            "--injection-file",
            "not_a_file",
            "--data-label",
            "TEST",
        ]
        with self.assertRaises(FileNotFoundError):
            self.inputs = DataGenerationInput(*parse_args(args_list, self.parser))

    def test_generation_seed_increases_with_injection_index(self):
        """Assert that generation seed increments for each job.

        ie
        JOB 0 -- seed X
        JOB 1 -- seed X + 1
        ...
        JOB N -- seed X + N

        This is so that the gaussian data for each job will be different.
        """
        idx = 0
        generation_seed = 0
        args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            f"--generation-seed={generation_seed}",
            f"--idx={idx}",
            "--gaussian-noise",
            "--trigger-time",
            "2",
            "--outdir",
            self.outdir,
            "--label",
            "TEST",
        ]
        self.inputs = DataGenerationInput(*parse_args(args_list, self.parser))
        self.assertEqual(self.inputs.generation_seed, idx + generation_seed)
        idx = 2
        generation_seed = 0
        args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            f"--generation-seed={generation_seed}",
            f"--idx={idx}",
            "--gaussian-noise",
            "--trigger-time",
            "1126259462",
            "--outdir",
            self.outdir,
            "--label",
            "TEST",
        ]
        self.inputs = DataGenerationInput(*parse_args(args_list, self.parser))
        self.assertEqual(self.inputs.generation_seed, idx + generation_seed)

    def test_generation_seed_is_random_if_none_provided(self):
        """Assert that the generation seed is some random value if not provided."""
        idx = 0
        generation_seed = None
        args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            f"--generation-seed={generation_seed}",
            f"--idx={idx}",
            "--gaussian-noise",
            "--trigger-time",
            "1126259462",
            "--outdir",
            self.outdir,
            "--label",
            "TEST",
        ]
        self.inputs = DataGenerationInput(*parse_args(args_list, self.parser))
        self.assertTrue(1 <= self.inputs.generation_seed <= 1e6)

    @mock.patch("bilby_pipe.data_generation.DataGenerationInput._get_data")
    @mock.patch("bilby.gw.detector.inject_signal_into_gwpy_timeseries")
    def test_inject_signal_into_time_domain_data(
        self, inject_signal_into_timeseries_method, get_data_method
    ):
        timeseries, metadata = load_test_strain_data()

        get_data_method.return_value = timeseries
        inject_signal_into_timeseries_method.return_value = (timeseries, metadata)
        args_list = ["tests/test_injection.ini", "--outdir", self.outdir]

        inputs = DataGenerationInput(*parse_args(args_list, self.parser))
        self.assertTrue(inputs.injection_parameters["geocent_time"] == 0)
        self.assertEqual(inject_signal_into_timeseries_method.call_count, 2)
        self.assertTrue(get_data_method.called)

        t0 = 1126259463.4
        t1 = t0 + 1

        t0_psd = t0 - 32
        t1_psd = t0

        get_data_method.assert_any_call("H1", "GWOSC", t0, t1)  # SIGNAL
        get_data_method.assert_any_call("H1", "GWOSC", t0_psd, t1_psd)  # PSD
        get_data_method.assert_any_call("L1", "GWOSC", t0, t1)  # SIGNAL
        get_data_method.assert_any_call("L1", "GWOSC", t0_psd, t1_psd)  # PSD

    def test_inject_signal_into_gaussian_noise(self):
        args_list = [
            "tests/test_injection_in_gaussian_noise.ini",
            "--outdir",
            self.outdir,
        ]
        data_input = DataGenerationInput(*parse_args(args_list, self.parser))
        injection_param = data_input.injection_parameters
        self.assertTrue(injection_param["geocent_time"] == 0)

    @mock.patch("bilby_pipe.data_generation.DataGenerationInput._gwpy_get")
    @mock.patch("bilby_pipe.data_generation.DataGenerationInput._is_gwpy_data_good")
    @mock.patch("bilby_pipe.data_generation.logger")
    def test_data_quality_ignore_flag(self, mock_logs, is_data_good, get_data_method):
        timeseries, _ = load_test_strain_data()
        is_data_good.return_value = False
        get_data_method.return_value = timeseries

        args_list = [
            "tests/test_basic_ini.ini",
            "--detectors",
            "[H1, L1]",
            "--channel-dict",
            "{'H1': 'GDS-CALIB_STRAIN', 'L1': 'GDS-CALIB_STRAIN'}",
            "--duration",
            " 1",
            "--prior_file",
            "tests/example_prior.prior",
            "--waveform-approximant",
            "IMRPhenomPv2",
            "--idx",
            "0",
            "--trigger_time",
            "1126259462.4",
            "--label",
            "QUALITY_TEST",
        ]

        # make sure that when the flag is present, no error
        args, unknown = parse_args(args_list, create_generation_parser())
        args.trigger_time = 1126259462.4
        input = DataGenerationInput(args, unknown)
        self.assertFalse(input._is_gwpy_data_good())
        self.assertTrue(input.ignore_gwpy_data_quality_check)

        # make sure that when the flag is not present, error present
        args, unknown = parse_args(args_list, create_generation_parser())
        args.trigger_time = 1126259462.4
        args.ignore_gwpy_data_quality_check = False
        with self.assertRaises(BilbyPipeError):
            DataGenerationInput(args, unknown)
            self.assertFalse(input._is_gwpy_data_good())
            self.assertFalse(input.ignore_gwpy_data_quality_check)

    @mock.patch("gwpy.segments.DataQualityFlag.query")
    @mock.patch("bilby_pipe.data_generation.logger")
    def test_data_quality_fail(self, mock_logs, quality_query):
        """Test the data quality check function's FAIL state.

        Parameters
        ----------
        mock_logs: the logging module being used inside this function

        """
        full_data = gwpy.segments.DataQualityFlag.read("tests/DATA/data_quality.hdf5")
        start_time_bad, end_time_bad = 1241725028.9, 1241725029.1
        quality_query.return_value = full_data
        data_is_good = DataGenerationInput._is_gwpy_data_good(
            start_time=start_time_bad, end_time=end_time_bad, det="H1"
        )
        self.assertFalse(data_is_good)
        self.assertTrue(mock_logs.warning.called)
        warning_log_str = mock_logs.warning.call_args.args[0]
        self.assertTrue("Data quality check: FAILED" in warning_log_str)

    @mock.patch("gwpy.segments.DataQualityFlag.query")
    @mock.patch("bilby_pipe.data_generation.logger")
    def test_data_quality_pass(self, mock_logs, quality_query):
        """Test the data quality function's PASS state.

        Parameters
        ----------
        mock_logs: the logging module being used inside this function

        """
        full_data = gwpy.segments.DataQualityFlag.read("tests/DATA/data_quality.hdf5")
        start_time_good, end_time_good = 1241725028.9, 1241725029
        quality_query.return_value = full_data
        data_is_good = DataGenerationInput._is_gwpy_data_good(
            start_time=start_time_good, end_time=end_time_good, det="H1"
        )
        self.assertTrue(data_is_good)
        self.assertFalse(mock_logs.warning.called)

    @mock.patch("gwpy.segments.DataQualityFlag.query")
    @mock.patch("bilby_pipe.data_generation.logger")
    def test_data_quality_exception(self, mock_logs, quality_query):
        """Test the data quality function's PASS state.

        Parameters
        ----------
        mock_logs: the logging module being used inside this function

        """
        start_time_good, end_time_good = 1241725028.9, 1241725029
        quality_query.side_effect = Exception("Some exception from GWpy")
        data_is_good = DataGenerationInput._is_gwpy_data_good(
            start_time=start_time_good, end_time=end_time_good, det="H1"
        )
        self.assertTrue(data_is_good is None)
        self.assertTrue(mock_logs.warning.called)


class TestDataReading(unittest.TestCase):
    def setUp(self):
        self.outdir = "test_outdir"
        self.data_dir = "tests/DATA/"
        self.default_args_list = [
            "--ini",
            "tests/test_data_generation.ini",
            "--outdir",
            self.outdir,
            "--data-label",
            "TEST",
        ]
        self.parser = create_generation_parser()
        self.inputs = DataGenerationInput(
            *parse_args(self.default_args_list, self.parser), create_data=False
        )

        self.det = "H1"
        self.channel = "H1:DCS-CALIB_STRAIN_C02"
        self.start_time = 1126259356.0
        self.end_time = 1126259357.0

    def tearDown(self):
        del self.inputs
        if os.path.isdir(self.outdir):
            shutil.rmtree(self.outdir)

    def test_read_data_gwf(self):
        self.inputs.data_dict = {self.det: f"{self.data_dir}/test_data.gwf"}
        data = self.inputs._gwpy_read(
            self.det, self.channel, self.start_time, self.end_time
        )
        self.assertEqual(data.times[0].value, self.start_time)
        self.assertEqual(len(data), 16384)

    def test_read_data_txt(self):
        self.inputs.data_dict = {self.det: f"{self.data_dir}/test_data.txt"}
        data = self.inputs._gwpy_read(
            self.det, self.channel, self.start_time, self.end_time
        )
        self.assertEqual(data.times[0].value, self.start_time)
        self.assertEqual(len(data), 16384)

    def test_read_data_hdf5(self):
        self.inputs.data_dict = {self.det: f"{self.data_dir}/test_data.hdf5"}
        data = self.inputs._gwpy_read(
            self.det, self.channel, self.start_time, self.end_time
        )
        self.assertEqual(data.times[0].value, self.start_time)
        self.assertEqual(len(data), 16384)


def load_test_strain_data():
    """Helper function to load data from gwpy_data.pickle"""
    ifo = DataDump.from_pickle("tests/DATA/gwpy_data.pickle").interferometers[0]
    timeseries = ifo.strain_data.to_gwpy_timeseries()
    metadata = ifo.meta_data
    return timeseries, metadata


if __name__ == "__main__":
    unittest.main()
