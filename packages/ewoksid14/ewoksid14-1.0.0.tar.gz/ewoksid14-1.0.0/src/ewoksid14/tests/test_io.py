import numpy

from ..tasks import io


def test_io_spec():
    mca = numpy.arange(6)
    mca_string = io.mca_data_to_spec_string(mca, date="start_date")
    expected = [
        "#F unspecified",
        "#D start_date",
        "",
        "#S ct",
        "#D start_date",
        "#N 1",
        "#@MCA 16C",
        "#@CHANN 6 0 5 1",
        "#@CALIB 0 1 0",
        "#@MCA_NB 1",
        "#L MCA0",
        "@A 0 1 2 3 4 5",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(16)
    mca_string = io.mca_data_to_spec_string(mca, date="start_date")
    expected = [
        "#F unspecified",
        "#D start_date",
        "",
        "#S ct",
        "#D start_date",
        "#N 1",
        "#@MCA 16C",
        "#@CHANN 16 0 15 1",
        "#@CALIB 0 1 0",
        "#@MCA_NB 1",
        "#L MCA0",
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(32)
    mca_string = io.mca_data_to_spec_string(mca, date="start_date")
    expected = [
        "#F unspecified",
        "#D start_date",
        "",
        "#S ct",
        "#D start_date",
        "#N 1",
        "#@MCA 16C",
        "#@CHANN 32 0 31 1",
        "#@CALIB 0 1 0",
        "#@MCA_NB 1",
        "#L MCA0",
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\\",
        " 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(33)
    mca_string = io.mca_data_to_spec_string(mca, date="start_date")
    expected = [
        "#F unspecified",
        "#D start_date",
        "",
        "#S ct",
        "#D start_date",
        "#N 1",
        "#@MCA 16C",
        "#@CHANN 33 0 32 1",
        "#@CALIB 0 1 0",
        "#@MCA_NB 1",
        "#L MCA0",
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\\",
        " 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\\",
        " 32",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(33)
    mca_string = io.mca_data_to_spec_string(
        mca, date="start_date", metadata={"a": 1, "b": 2}
    )
    expected = [
        "#F unspecified",
        "#D start_date",
        "",
        "#S ct",
        "#D start_date",
        "#C a = 1",
        "#C b = 2",
        "#N 1",
        "#@MCA 16C",
        "#@CHANN 33 0 32 1",
        "#@CALIB 0 1 0",
        "#@MCA_NB 1",
        "#L MCA0",
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\\",
        " 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\\",
        " 32",
        "",
    ]
    assert mca_string.split("\n") == expected
