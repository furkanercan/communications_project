import numpy as np
from src.rx.decoders.polar.sc import PolarDecoder_SC

def test_decoder_initialization():
    # Parameters
    len_logn = 3
    vec_llr = np.random.randn(2**len_logn)  # Random LLR values
    vec_isfrozen = [1, 0, 1, 0, 0, 1, 0, 1]  # Example frozen bit vector
    qbits_enable = False
    quant_intl_max = 7
    quant_intl_min = -7

    # Initialize the decoder
    decoder = PolarDecoder_SC(vec_llr, len_logn, vec_isfrozen, qbits_enable, quant_intl_max, quant_intl_min)

    # Test attribute initialization
    assert decoder.len_logn == len_logn
    assert len(decoder.vec_llr) == 2**len_logn
    assert decoder.vec_isfrozen == vec_isfrozen
    assert decoder.qbits_enable == qbits_enable
    assert decoder.quant_intl_max == quant_intl_max
    assert decoder.quant_intl_min == quant_intl_min

def test_create_decoding_schedule():
    # Parameters
    len_logn = 3
    vec_llr = np.random.randn(2**len_logn)  # Random LLR values
    vec_isfrozen = [1, 0, 1, 0, 0, 1, 0, 1]  # Example frozen bit vector
    qbits_enable = False
    quant_intl_max = 7
    quant_intl_min = -7

    # Initialize the decoder
    decoder = PolarDecoder_SC(vec_llr, len_logn, vec_isfrozen, qbits_enable, quant_intl_max, quant_intl_min)

    # Test schedule creation
    decoder.initialize_decoder()
    assert len(decoder.vec_dec_sch) > 0, "Decoding schedule should not be empty."
    assert len(decoder.vec_dec_sch_size) == len(decoder.vec_dec_sch), "Size vector length mismatch."
    assert len(decoder.vec_dec_sch_depth) == len(decoder.vec_dec_sch), "Depth vector length mismatch."
    assert len(decoder.vec_dec_sch_dir) == len(decoder.vec_dec_sch), "Direction vector length mismatch."

def test_dec_sc_f():
    # Parameters
    len_logn = 3
    vec_llr = np.random.randn(2**len_logn)  # Random LLR values
    vec_isfrozen = [1, 0, 1, 0, 0, 1, 0, 1]  # Example frozen bit vector
    qbits_enable = True
    quant_intl_max = 7
    quant_intl_min = -7

    # Initialize the decoder
    decoder = PolarDecoder_SC(vec_llr, len_logn, vec_isfrozen, qbits_enable, quant_intl_max, quant_intl_min)
    decoder.initialize_decoder()

    # Example inputs for dec_sc_f
    stage_size = 4
    stage_depth = 2
    decoder.mem_alpha[stage_depth] = np.array([2.0, -3.0, 1.0, -1.0])  # Set example alpha values

    # Perform F-node computation
    decoder.dec_sc_f(stage_size, stage_depth, is_quantized=True, max_value=quant_intl_max)

    # Check the results
    expected_result = np.array([1.0, 1.0])  # Expected output after F-node computation
    np.testing.assert_array_almost_equal(
        decoder.mem_alpha[stage_depth - 1][:stage_size // 2],
        expected_result,
        decimal=1,
        err_msg="F-node computation failed."
    )

def test_dec_sc():
    # Parameters
    len_logn = 3
    vec_llr = np.random.randn(2**len_logn)  # Random LLR values
    vec_isfrozen = [1, 0, 1, 0, 0, 1, 0, 1]  # Example frozen bit vector
    qbits_enable = False
    quant_intl_max = 7
    quant_intl_min = -7

    # Initialize the decoder
    decoder = PolarDecoder_SC(vec_llr, len_logn, vec_isfrozen, qbits_enable, quant_intl_max, quant_intl_min)
    decoder.initialize_decoder()

    # Test decoding
    vec_decoded = decoder.dec_sc(qbits_enable, quant_intl_max, quant_intl_min)

    # Check the length of the decoded vector
    num_info_bits = sum(1 for bit in vec_isfrozen if bit == 0)
    assert len(vec_decoded) == num_info_bits, "Decoded vector length mismatch."
