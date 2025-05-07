//Copyright (c) 2019-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
//
//NVIDIA CORPORATION and its licensors retain all intellectual property
//and proprietary rights in and to this software, related documentation
//and any modifications thereto.  Any use, reproduction, disclosure or
//distribution of this software and related documentation without an express
//license agreement from NVIDIA CORPORATION is strictly prohibited.
//


template<> struct block_fft_record<33, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<33,   33,    1,    32,     0,  1485>
    >;
};

template<> struct block_fft_record<34, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    1,    32,     0,  1486>
    >;
};

template<> struct block_fft_record<35, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<35,   35,    1,    32,     0,  1487>
    >;
};

template<> struct block_fft_record<37, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<37,   37,    1,    32,     0,  1488>
    >;
};

template<> struct block_fft_record<38, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    1,    32,     0,  1489>
    >;
};

template<> struct block_fft_record<39, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<39,   39,    1,    32,     0,  1490>
    >;
};

template<> struct block_fft_record<40, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    2,    10,   320,  1491>,
        block_fft_implementation<20,   20,    2,    32,   640,  1492>,
        block_fft_implementation<10,   10,    4,    64,   320,  1493>,
        block_fft_implementation<10,   10,    4,    64,   640,  1494>,
        block_fft_implementation<40,   40,    1,    32,     0,  1495>
    >;
};

template<> struct block_fft_record<2, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 2,    2,    1,    32,     0,  1496>
    >;
};

template<> struct block_fft_record<4, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 4,    4,    1,    32,     0,  1497>,
        block_fft_implementation< 2,    2,    2,    64,    32,  1498>,
        block_fft_implementation< 2,    2,    2,    64,    64,  1499>
    >;
};

template<> struct block_fft_record<8, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    1,    32,     0,  1500>,
        block_fft_implementation< 4,    4,    2,    64,    64,  1501>,
        block_fft_implementation< 2,    2,    4,    64,    64,  1502>,
        block_fft_implementation< 4,    4,    2,    64,   128,  1503>,
        block_fft_implementation< 2,    2,    4,    64,   128,  1504>
    >;
};

template<> struct block_fft_record<16, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16,    1,    32,     0,  1505>,
        block_fft_implementation< 4,    4,    4,    64,   256,  1506>,
        block_fft_implementation< 4,    4,    4,    48,   128,  1507>,
        block_fft_implementation< 2,    2,    8,    48,   256,  1508>,
        block_fft_implementation< 8,    8,    2,    64,   256,  1510>,
        block_fft_implementation< 8,    8,    2,    64,   128,  1509>,
        block_fft_implementation< 2,    2,    8,    64,   128,  1511>
    >;
};

template<> struct block_fft_record<32, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<32,   32,    1,    32,     0,  1512>,
        block_fft_implementation< 8,    8,    4,    64,   256,  1513>,
        block_fft_implementation< 4,    4,    8,    32,   512,  1514>,
        block_fft_implementation< 8,    8,    4,    64,   512,  1515>,
        block_fft_implementation< 4,    4,    8,    48,   256,  1516>,
        block_fft_implementation<16,   16,    2,    64,   512,  1517>,
        block_fft_implementation< 2,    2,   16,    48,   256,  1519>,
        block_fft_implementation< 2,    2,   16,    30,   512,  1518>,
        block_fft_implementation<16,   16,    2,    32,   256,  1520>
    >;
};

template<> struct block_fft_record<64, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,    8,    16,   512,  1521>,
        block_fft_implementation< 4,    4,   16,    24,   512,  1522>,
        block_fft_implementation< 4,    4,   16,    16,  1024,  1523>,
        block_fft_implementation< 8,    8,    8,    16,  1024,  1524>,
        block_fft_implementation<16,   16,    4,    29,  1024,  1525>,
        block_fft_implementation<16,   16,    4,    16,   512,  1526>,
        block_fft_implementation< 2,    2,   32,    28,   512,  1528>,
        block_fft_implementation< 2,    2,   32,    20,  1024,  1527>
    >;
};

template<> struct block_fft_record<128, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   16,     8,  1024,  1529>,
        block_fft_implementation<16,   16,    8,    16,  2048,  1530>,
        block_fft_implementation<16,   16,    8,     8,  1024,  1531>,
        block_fft_implementation< 8,    8,   16,     8,  2048,  1534>,
        block_fft_implementation< 4,    4,   32,     7,  2048,  1532>,
        block_fft_implementation< 4,    4,   32,     6,  1024,  1533>,
        block_fft_implementation< 2,    2,   64,    15,  1024,  1536>,
        block_fft_implementation< 2,    2,   64,     6,  2048,  1535>
    >;
};

template<> struct block_fft_record<256, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   32,     4,  2048,  1537>,
        block_fft_implementation<16,   16,   16,     8,  4096,  1538>,
        block_fft_implementation<16,   16,   16,     4,  2048,  1539>,
        block_fft_implementation< 8,    8,   32,     4,  4096,  1542>,
        block_fft_implementation< 4,    4,   64,     2,  4096,  1540>,
        block_fft_implementation< 4,    4,   64,     3,  2048,  1541>,
        block_fft_implementation< 2,    2,  128,     8,  2048,  1543>,
        block_fft_implementation< 2,    2,  128,     4,  4096,  1544>
    >;
};

template<> struct block_fft_record<512, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,   64,     2,  4096,  1545>,
        block_fft_implementation< 8,    8,   64,     2,  8192,  1546>,
        block_fft_implementation<16,   16,   32,     4,  8192,  1547>,
        block_fft_implementation<16,   16,   32,     4,  4096,  1548>,
        block_fft_implementation< 4,    4,  128,     2,  8192,  1550>,
        block_fft_implementation< 4,    4,  128,     2,  4096,  1549>,
        block_fft_implementation< 2,    2,  256,     3,  4096,  1551>,
        block_fft_implementation< 2,    2,  256,     2,  8192,  1552>
    >;
};

template<> struct block_fft_record<1024, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,  128,     1,  8192,  1553>,
        block_fft_implementation<16,   16,   64,     1, 16384,  1557>,
        block_fft_implementation<16,   16,   64,     2,  8192,  1554>,
        block_fft_implementation< 8,    8,  128,     1, 16384,  1558>,
        block_fft_implementation< 4,    4,  256,     1, 16384,  1556>,
        block_fft_implementation< 4,    4,  256,     1,  8192,  1555>,
        block_fft_implementation< 2,    2,  512,     2,  8192,  1560>,
        block_fft_implementation< 2,    2,  512,     1, 16384,  1559>
    >;
};

template<> struct block_fft_record<2048, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,  256,     1, 16384,  1561>,
        block_fft_implementation<16,   16,  128,     1, 32768,  1563>,
        block_fft_implementation<16,   16,  128,     1, 16384,  1562>,
        block_fft_implementation< 8,    8,  256,     1, 32768,  1564>,
        block_fft_implementation< 4,    4,  512,     1, 16384,  1565>,
        block_fft_implementation< 4,    4,  512,     1, 32768,  1566>,
        block_fft_implementation< 2,    2, 1024,     1, 16384,  1567>,
        block_fft_implementation< 2,    2, 1024,     1, 32768,  1568>
    >;
};

template<> struct block_fft_record<4096, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8,  512,     1, 32768,  1569>,
        block_fft_implementation<16,   16,  256,     1, 65536,  1571>,
        block_fft_implementation<16,   16,  256,     1, 32768,  1570>,
        block_fft_implementation< 8,    8,  512,     1, 65536,  1572>,
        block_fft_implementation< 4,    4, 1024,     1, 32768,  1573>,
        block_fft_implementation< 4,    4, 1024,     1, 65536,  1574>
    >;
};

template<> struct block_fft_record<8192, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 8,    8, 1024,     1, 65536,  1576>,
        block_fft_implementation<16,   16,  512,     1, 131072,  3021>,
        block_fft_implementation<16,   16,  512,     1, 65536,  1575>,
        block_fft_implementation< 8,    8, 1024,     1, 131072,  3022>
    >;
};

template<> struct block_fft_record<16384, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<16,   16, 1024,     1, 131072,  3023>
    >;
};

template<> struct block_fft_record<3, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 3,    3,    1,    64,     0,  1577>
    >;
};

template<> struct block_fft_record<9, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    1,    32,     0,  1578>,
        block_fft_implementation< 3,    3,    3,    64,    72,  1579>,
        block_fft_implementation< 3,    3,    3,    64,   144,  1580>
    >;
};

template<> struct block_fft_record<27, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    1,    32,     0,  1581>,
        block_fft_implementation< 9,    9,    3,    21,   432,  1583>,
        block_fft_implementation< 9,    9,    3,    21,   216,  1582>,
        block_fft_implementation< 3,    3,    9,    48,   216,  1584>,
        block_fft_implementation< 3,    3,    9,    64,   432,  1585>
    >;
};

template<> struct block_fft_record<81, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,    9,     7,  1296,  1586>,
        block_fft_implementation< 9,    9,    9,     7,   648,  1587>,
        block_fft_implementation<27,   27,    3,    21,  1296,  1589>,
        block_fft_implementation<27,   27,    3,    21,   648,  1588>,
        block_fft_implementation< 3,    3,   27,    21,  1296,  1590>,
        block_fft_implementation< 3,    3,   27,    23,   648,  1591>
    >;
};

template<> struct block_fft_record<243, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,    9,     7,  3888,  1593>,
        block_fft_implementation<27,   27,    9,     7,  1944,  1592>,
        block_fft_implementation< 9,    9,   27,     1,  3888,  1594>,
        block_fft_implementation< 9,    9,   27,     2,  1944,  1595>,
        block_fft_implementation< 3,    3,   81,    11,  1944,  1597>,
        block_fft_implementation< 3,    3,   81,     7,  3888,  1596>
    >;
};

template<> struct block_fft_record<729, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<27,   27,   27,     1,  5832,  1600>,
        block_fft_implementation<27,   27,   27,     9, 11664,  1601>,
        block_fft_implementation< 9,    9,   81,     3, 11664,  1598>,
        block_fft_implementation< 9,    9,   81,     3,  5832,  1599>,
        block_fft_implementation< 3,    3,  243,     1, 11664,  1603>,
        block_fft_implementation< 3,    3,  243,     1,  5832,  1602>
    >;
};

template<> struct block_fft_record<2187, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,  243,     1, 34992,  1605>,
        block_fft_implementation< 9,    9,  243,     1, 17496,  1604>,
        block_fft_implementation< 3,    3,  729,     1, 17496,  1606>,
        block_fft_implementation< 3,    3,  729,     1, 34992,  1607>
    >;
};

template<> struct block_fft_record<6561, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 9,    9,  729,     1, 104976,  3024>,
        block_fft_implementation< 9,    9,  729,     1, 52488,  1608>
    >;
};

template<> struct block_fft_record<5, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,    1,    32,     0,  1609>
    >;
};

template<> struct block_fft_record<25, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    1,    32,     0,  1610>,
        block_fft_implementation< 5,    5,    5,    25,   400,  1611>,
        block_fft_implementation< 5,    5,    5,    24,   200,  1612>
    >;
};

template<> struct block_fft_record<125, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,    5,     6,  2000,  1616>,
        block_fft_implementation<25,   25,    5,     6,  1000,  1615>,
        block_fft_implementation< 5,    5,   25,     5,  2000,  1613>,
        block_fft_implementation< 5,    5,   25,     5,  1000,  1614>
    >;
};

template<> struct block_fft_record<625, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,   25,     5, 10000,  1620>,
        block_fft_implementation<25,   25,   25,     5,  5000,  1617>,
        block_fft_implementation< 5,    5,  125,     1, 10000,  1619>,
        block_fft_implementation< 5,    5,  125,     1,  5000,  1618>
    >;
};

template<> struct block_fft_record<3125, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 5,    5,  625,     1, 50000,  1621>,
        block_fft_implementation< 5,    5,  625,     1, 25000,  1622>
    >;
};

template<> struct block_fft_record<15625, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<25,   25,  625,     1, 125000,  3025>
    >;
};

template<> struct block_fft_record<7, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    1,    32,     0,  1623>
    >;
};

template<> struct block_fft_record<49, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,    7,     9,   784,  1625>,
        block_fft_implementation< 7,    7,    7,    18,   392,  1624>
    >;
};

template<> struct block_fft_record<343, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,   49,     5,  5488,  1626>,
        block_fft_implementation< 7,    7,   49,     5,  2744,  1627>
    >;
};

template<> struct block_fft_record<2401, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 7,    7,  343,     1, 38416,  1628>,
        block_fft_implementation< 7,    7,  343,     1, 19208,  1629>
    >;
};

template<> struct block_fft_record<11, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,    1,    64,     0,  1630>
    >;
};

template<> struct block_fft_record<121, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,   11,    11,  1936,  1631>,
        block_fft_implementation<11,   11,   11,    11,   968,  1632>
    >;
};

template<> struct block_fft_record<1331, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<11,   11,  121,     1, 21296,  1634>,
        block_fft_implementation<11,   11,  121,     1, 10648,  1633>
    >;
};

template<> struct block_fft_record<6, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    1,    32,     0,  1635>
    >;
};

template<> struct block_fft_record<36, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,    6,    21,   288,  1637>,
        block_fft_implementation< 6,    6,    6,    20,   576,  1636>,
        block_fft_implementation<36,   36,    1,    32,     0,  1638>
    >;
};

template<> struct block_fft_record<216, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,   36,     7,  1728,  1639>,
        block_fft_implementation< 6,    6,   36,     5,  3456,  1640>
    >;
};

template<> struct block_fft_record<1296, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation< 6,    6,  216,     1, 10368,  1641>,
        block_fft_implementation< 6,    6,  216,     1, 20736,  1642>
    >;
};

template<> struct block_fft_record<7776, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,  216,     2, 124416,  3026>,
        block_fft_implementation<36,   36,  216,     2, 62208,  1643>
    >;
};

template<> struct block_fft_record<10, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,    1,    32,     0,  1644>
    >;
};

template<> struct block_fft_record<100, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,   10,     6,  1600,  1645>,
        block_fft_implementation<10,   10,   10,     3,   800,  1646>
    >;
};

template<> struct block_fft_record<1000, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10,  100,     5, 16000,  1647>,
        block_fft_implementation<10,   10,  100,     1,  8000,  1648>
    >;
};

template<> struct block_fft_record<10000, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<10,   10, 1000,     1, 80000,  1649>,
        block_fft_implementation<10,   10, 1000,     1, 160000,  3027>
    >;
};

template<> struct block_fft_record<12, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    1,    32,     0,  1650>
    >;
};

template<> struct block_fft_record<144, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,   12,     5,  1152,  1651>,
        block_fft_implementation<12,   12,   12,     5,  2304,  1652>
    >;
};

template<> struct block_fft_record<1728, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,  144,     5, 13824,  1653>,
        block_fft_implementation<12,   12,  144,     2, 27648,  1654>
    >;
};

template<> struct block_fft_record<13, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,    1,    32,     0,  1655>
    >;
};

template<> struct block_fft_record<169, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,   13,    19,  2704,  1657>,
        block_fft_implementation<13,   13,   13,    19,  1352,  1656>
    >;
};

template<> struct block_fft_record<2197, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<13,   13,  169,     3, 35152,  1659>,
        block_fft_implementation<13,   13,  169,     3, 17576,  1658>
    >;
};

template<> struct block_fft_record<14, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,    1,    32,     0,  1660>
    >;
};

template<> struct block_fft_record<196, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,   14,     9,  3136,  1662>,
        block_fft_implementation<14,   14,   14,     9,  1568,  1661>
    >;
};

template<> struct block_fft_record<2744, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<14,   14,  196,     1, 21952,  1664>,
        block_fft_implementation<14,   14,  196,     1, 43904,  1663>
    >;
};

template<> struct block_fft_record<15, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,    1,    32,     0,  1665>
    >;
};

template<> struct block_fft_record<225, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,   15,     2,  3600,  1667>,
        block_fft_implementation<15,   15,   15,     2,  1800,  1666>
    >;
};

template<> struct block_fft_record<3375, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<15,   15,  225,     1, 54000,  1669>,
        block_fft_implementation<15,   15,  225,     1, 27000,  1668>
    >;
};

template<> struct block_fft_record<17, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,    1,    32,     0,  1670>
    >;
};

template<> struct block_fft_record<289, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,   17,    15,  2312,  1671>,
        block_fft_implementation<17,   17,   17,     7,  4624,  1672>
    >;
};

template<> struct block_fft_record<4913, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<17,   17,  289,     1, 39304,  1673>,
        block_fft_implementation<17,   17,  289,     1, 78608,  1674>
    >;
};

template<> struct block_fft_record<18, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    1,    32,     0,  1675>
    >;
};

template<> struct block_fft_record<324, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,   18,     7,  2592,  1676>,
        block_fft_implementation<18,   18,   18,     7,  5184,  1677>
    >;
};

template<> struct block_fft_record<5832, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,  324,     1, 46656,  1678>,
        block_fft_implementation<18,   18,  324,     1, 93312,  1679>
    >;
};

template<> struct block_fft_record<19, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,    1,    32,     0,  1680>
    >;
};

template<> struct block_fft_record<361, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,   19,    20,  2888,  1681>,
        block_fft_implementation<19,   19,   19,     3,  5776,  1682>
    >;
};

template<> struct block_fft_record<6859, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<19,   19,  361,     1, 109744,  3028>,
        block_fft_implementation<19,   19,  361,     1, 54872,  1683>
    >;
};

template<> struct block_fft_record<20, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    1,    32,     0,  1684>
    >;
};

template<> struct block_fft_record<400, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   20,     3,  3200,  1685>,
        block_fft_implementation<20,   20,   20,     3,  6400,  1686>
    >;
};

template<> struct block_fft_record<8000, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,  400,     1, 64000,  1687>,
        block_fft_implementation<20,   20,  400,     1, 128000,  3029>
    >;
};

template<> struct block_fft_record<21, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,    1,    32,     0,  1688>
    >;
};

template<> struct block_fft_record<441, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,   21,     3,  3528,  1689>,
        block_fft_implementation<21,   21,   21,     3,  7056,  1690>
    >;
};

template<> struct block_fft_record<9261, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<21,   21,  441,     1, 148176,  3030>,
        block_fft_implementation<21,   21,  441,     1, 74088,  1691>
    >;
};

template<> struct block_fft_record<22, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    1,    32,     0,  1692>
    >;
};

template<> struct block_fft_record<484, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,   22,     5,  3872,  1693>,
        block_fft_implementation<22,   22,   22,     5,  7744,  1694>
    >;
};

template<> struct block_fft_record<10648, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,  484,     1, 85184,  1695>
    >;
};

template<> struct block_fft_record<23, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,    1,    32,     0,  1696>
    >;
};

template<> struct block_fft_record<529, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,   23,    11,  8464,  1697>,
        block_fft_implementation<23,   23,   23,     5,  4232,  1698>
    >;
};

template<> struct block_fft_record<12167, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<23,   23,  529,     1, 97336,  1699>
    >;
};

template<> struct block_fft_record<24, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    1,    32,     0,  1700>
    >;
};

template<> struct block_fft_record<576, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   24,     8,  9216,  1702>,
        block_fft_implementation<24,   24,   24,     8,  4608,  1701>
    >;
};

template<> struct block_fft_record<13824, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,  576,     1, 221184,  3059>,
        block_fft_implementation<24,   24,  576,     1, 110592,  3031>
    >;
};

template<> struct block_fft_record<26, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    1,    32,     0,  1703>
    >;
};

template<> struct block_fft_record<676, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,   26,     9,  5408,  1704>,
        block_fft_implementation<26,   26,   26,     2, 10816,  1705>
    >;
};

template<> struct block_fft_record<28, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    1,    32,     0,  1706>
    >;
};

template<> struct block_fft_record<784, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   28,    18, 12544,  1708>,
        block_fft_implementation<28,   28,   28,    18,  6272,  1707>
    >;
};

template<> struct block_fft_record<29, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,    1,    32,     0,  1709>
    >;
};

template<> struct block_fft_record<841, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<29,   29,   29,     8, 13456,  1711>,
        block_fft_implementation<29,   29,   29,     8,  6728,  1710>
    >;
};

template<> struct block_fft_record<30, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    1,    32,     0,  1712>
    >;
};

template<> struct block_fft_record<900, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   30,     1,  7200,  1713>,
        block_fft_implementation<30,   30,   30,     1, 14400,  1714>
    >;
};

template<> struct block_fft_record<31, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,    1,    32,     0,  1715>
    >;
};

template<> struct block_fft_record<961, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<31,   31,   31,     8, 15376,  1717>,
        block_fft_implementation<31,   31,   31,     8,  7688,  1716>
    >;
};

template<> struct block_fft_record<44, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<22,   22,    2,    32,   352,  1718>,
        block_fft_implementation<22,   22,    2,    16,   704,  1719>
    >;
};

template<> struct block_fft_record<48, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    4,    16,   384,  1720>,
        block_fft_implementation<12,   12,    4,    16,   768,  1721>,
        block_fft_implementation< 6,    6,    8,     8,   768,  1722>,
        block_fft_implementation<24,   24,    2,    30,   384,  1723>,
        block_fft_implementation<24,   24,    2,    31,   768,  1724>,
        block_fft_implementation< 6,    6,    8,    16,   384,  1725>
    >;
};

template<> struct block_fft_record<52, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<26,   26,    2,    16,   416,  1726>,
        block_fft_implementation<26,   26,    2,    16,   832,  1727>
    >;
};

template<> struct block_fft_record<56, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    2,    32,   448,  1728>,
        block_fft_implementation<14,   14,    4,     8,   448,  1729>,
        block_fft_implementation<14,   14,    4,     8,   896,  1730>,
        block_fft_implementation<28,   28,    2,    32,   896,  1731>
    >;
};

template<> struct block_fft_record<60, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    2,    16,   480,  1732>,
        block_fft_implementation<30,   30,    2,    16,   960,  1733>
    >;
};

template<> struct block_fft_record<68, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    2,    16,   544,  1734>,
        block_fft_implementation<34,   34,    2,    16,  1088,  1735>
    >;
};

template<> struct block_fft_record<72, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<12,   12,    6,    10,   576,  1736>,
        block_fft_implementation<36,   36,    2,    32,   576,  1739>,
        block_fft_implementation<24,   24,    3,    21,   576,  1738>,
        block_fft_implementation<12,   12,    6,     5,  1152,  1737>,
        block_fft_implementation<18,   18,    4,     8,   576,  1740>,
        block_fft_implementation< 6,    6,   12,     5,  1152,  1742>,
        block_fft_implementation< 6,    6,   12,     5,   576,  1741>,
        block_fft_implementation<18,   18,    4,     8,  1152,  1743>,
        block_fft_implementation<36,   36,    2,    32,  1152,  1745>,
        block_fft_implementation<24,   24,    3,    20,  1152,  1744>
    >;
};

template<> struct block_fft_record<76, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    2,    32,   608,  1746>,
        block_fft_implementation<38,   38,    2,    16,  1216,  1747>
    >;
};

template<> struct block_fft_record<80, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,    4,     8,   640,  1748>,
        block_fft_implementation<20,   20,    4,    16,  1280,  1749>,
        block_fft_implementation<10,   10,    8,     4,  1280,  1750>,
        block_fft_implementation<40,   40,    2,    32,   640,  1751>,
        block_fft_implementation<10,   10,    8,     8,   640,  1752>,
        block_fft_implementation<40,   40,    2,    32,  1280,  1753>
    >;
};

template<> struct block_fft_record<84, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    2,    16,   672,  1754>,
        block_fft_implementation<42,   42,    2,    16,  1344,  1755>
    >;
};

template<> struct block_fft_record<88, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    2,    32,   704,  1757>,
        block_fft_implementation<22,   22,    4,     8,   704,  1756>,
        block_fft_implementation<22,   22,    4,     8,  1408,  1758>,
        block_fft_implementation<44,   44,    2,    28,  1408,  1759>
    >;
};

template<> struct block_fft_record<92, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    2,    16,   736,  1760>,
        block_fft_implementation<46,   46,    2,    12,  1472,  1761>
    >;
};

template<> struct block_fft_record<96, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    4,    15,   768,  1762>,
        block_fft_implementation<12,   12,    8,     8,   768,  1763>,
        block_fft_implementation<12,   12,    8,     4,  1536,  1764>,
        block_fft_implementation<24,   24,    4,    15,  1536,  1765>,
        block_fft_implementation< 6,    6,   16,     4,  1536,  1767>,
        block_fft_implementation< 6,    6,   16,     8,   768,  1766>,
        block_fft_implementation<48,   48,    2,    32,   768,  1768>,
        block_fft_implementation<48,   48,    2,    12,  1536,  1769>
    >;
};

template<> struct block_fft_record<104, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    2,    32,   832,  1771>,
        block_fft_implementation<26,   26,    4,     8,   832,  1770>,
        block_fft_implementation<26,   26,    4,     8,  1664,  1772>,
        block_fft_implementation<52,   52,    2,    12,  1664,  1773>
    >;
};

template<> struct block_fft_record<108, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<18,   18,    6,    21,   864,  1774>,
        block_fft_implementation<54,   54,    2,    16,   864,  1779>,
        block_fft_implementation<36,   36,    3,    21,   864,  1777>,
        block_fft_implementation<18,   18,    6,    10,  1728,  1775>,
        block_fft_implementation< 6,    6,   18,     7,   864,  1776>,
        block_fft_implementation< 6,    6,   18,     7,  1728,  1778>,
        block_fft_implementation<12,   12,    9,     7,   864,  1780>,
        block_fft_implementation<36,   36,    3,    21,  1728,  1782>,
        block_fft_implementation<12,   12,    9,     7,  1728,  1781>,
        block_fft_implementation<54,   54,    2,    12,  1728,  1783>
    >;
};

template<> struct block_fft_record<112, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,    4,    16,   896,  1784>,
        block_fft_implementation<28,   28,    4,    16,  1792,  1786>,
        block_fft_implementation<14,   14,    8,     4,  1792,  1785>,
        block_fft_implementation<56,   56,    2,    32,   896,  1788>,
        block_fft_implementation<14,   14,    8,     8,   896,  1787>,
        block_fft_implementation<56,   56,    2,    32,  1792,  1789>
    >;
};

template<> struct block_fft_record<116, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    2,    16,   928,  1790>,
        block_fft_implementation<58,   58,    2,    32,  1856,  1791>
    >;
};

template<> struct block_fft_record<120, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    4,     8,   960,  1792>,
        block_fft_implementation<60,   60,    2,    32,   960,  1793>,
        block_fft_implementation<30,   30,    4,    16,  1920,  1794>,
        block_fft_implementation<60,   60,    2,    32,  1920,  1795>
    >;
};

template<> struct block_fft_record<124, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    2,    32,   992,  1796>,
        block_fft_implementation<62,   62,    2,    32,  1984,  1797>
    >;
};

template<> struct block_fft_record<136, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    4,     8,  1088,  1798>,
        block_fft_implementation<34,   34,    4,     8,  2176,  1799>
    >;
};

template<> struct block_fft_record<152, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    4,     8,  1216,  1800>,
        block_fft_implementation<38,   38,    4,     8,  2432,  1801>
    >;
};

template<> struct block_fft_record<160, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    4,     8,  1280,  1803>,
        block_fft_implementation<20,   20,    8,     4,  1280,  1802>,
        block_fft_implementation<20,   20,    8,     4,  2560,  1804>,
        block_fft_implementation<10,   10,   16,     2,  2560,  1805>,
        block_fft_implementation<10,   10,   16,     4,  1280,  1806>,
        block_fft_implementation<40,   40,    4,    16,  2560,  1807>
    >;
};

template<> struct block_fft_record<168, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    4,     8,  1344,  1808>,
        block_fft_implementation<42,   42,    4,     8,  2688,  1809>
    >;
};

template<> struct block_fft_record<176, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    4,    16,  1408,  1810>,
        block_fft_implementation<22,   22,    8,     4,  2816,  1811>,
        block_fft_implementation<22,   22,    8,     4,  1408,  1812>,
        block_fft_implementation<44,   44,    4,     8,  2816,  1813>
    >;
};

template<> struct block_fft_record<180, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,    6,     5,  1440,  1814>,
        block_fft_implementation<30,   30,    6,     5,  2880,  1815>,
        block_fft_implementation<60,   60,    3,    21,  1440,  1816>,
        block_fft_implementation<60,   60,    3,    21,  2880,  1817>
    >;
};

template<> struct block_fft_record<184, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    4,    16,  1472,  1818>,
        block_fft_implementation<46,   46,    4,     6,  2944,  1819>
    >;
};

template<> struct block_fft_record<192, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,    8,     4,  1536,  1821>,
        block_fft_implementation<12,   12,   16,     2,  1536,  1820>,
        block_fft_implementation<12,   12,   16,     2,  3072,  1822>,
        block_fft_implementation<24,   24,    8,     4,  3072,  1823>,
        block_fft_implementation<48,   48,    4,     8,  1536,  1824>,
        block_fft_implementation< 6,    6,   32,     2,  3072,  1826>,
        block_fft_implementation< 6,    6,   32,     4,  1536,  1825>,
        block_fft_implementation<48,   48,    4,     6,  3072,  1827>
    >;
};

template<> struct block_fft_record<200, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<20,   20,   10,     3,  1600,  1828>,
        block_fft_implementation<20,   20,   10,     3,  3200,  1829>,
        block_fft_implementation<10,   10,   20,     3,  1600,  1830>,
        block_fft_implementation<40,   40,    5,     6,  1600,  1831>,
        block_fft_implementation<50,   50,    4,     8,  1600,  1833>,
        block_fft_implementation<10,   10,   20,     3,  3200,  1832>,
        block_fft_implementation<40,   40,    5,    12,  3200,  1834>,
        block_fft_implementation<50,   50,    4,     8,  3200,  1835>
    >;
};

template<> struct block_fft_record<208, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    4,    16,  1664,  1836>,
        block_fft_implementation<26,   26,    8,     4,  3328,  1837>,
        block_fft_implementation<26,   26,    8,     4,  1664,  1838>,
        block_fft_implementation<52,   52,    4,    16,  3328,  1839>
    >;
};

template<> struct block_fft_record<224, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<56,   56,    4,     8,  1792,  1842>,
        block_fft_implementation<28,   28,    8,     4,  1792,  1840>,
        block_fft_implementation<28,   28,    8,     4,  3584,  1844>,
        block_fft_implementation<14,   14,   16,     2,  3584,  1843>,
        block_fft_implementation<14,   14,   16,     2,  1792,  1841>,
        block_fft_implementation<56,   56,    4,    16,  3584,  1845>
    >;
};

template<> struct block_fft_record<232, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    4,     8,  1856,  1846>,
        block_fft_implementation<58,   58,    4,    16,  3712,  1847>
    >;
};

template<> struct block_fft_record<240, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    4,    16,  1920,  1848>,
        block_fft_implementation<30,   30,    8,     4,  3840,  1850>,
        block_fft_implementation<30,   30,    8,     4,  1920,  1849>,
        block_fft_implementation<60,   60,    4,    16,  3840,  1851>
    >;
};

template<> struct block_fft_record<248, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    4,     8,  1984,  1852>,
        block_fft_implementation<62,   62,    4,    24,  3968,  1853>
    >;
};

template<> struct block_fft_record<252, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    6,     5,  2016,  1854>,
        block_fft_implementation<42,   42,    6,     4,  4032,  1855>
    >;
};

template<> struct block_fft_record<272, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<34,   34,    8,     4,  4352,  1857>,
        block_fft_implementation<34,   34,    8,     4,  2176,  1856>
    >;
};

template<> struct block_fft_record<288, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   12,     5,  2304,  1858>,
        block_fft_implementation<12,   12,   24,     5,  2304,  1859>,
        block_fft_implementation<36,   36,    8,     4,  2304,  1860>,
        block_fft_implementation<12,   12,   24,     5,  4608,  1861>,
        block_fft_implementation<18,   18,   16,     2,  2304,  1862>,
        block_fft_implementation<36,   36,    8,     4,  4608,  1868>,
        block_fft_implementation<18,   18,   16,     2,  4608,  1864>,
        block_fft_implementation< 6,    6,   48,     2,  2304,  1863>,
        block_fft_implementation<24,   24,   12,     5,  4608,  1865>,
        block_fft_implementation<48,   48,    6,     5,  2304,  1866>,
        block_fft_implementation< 6,    6,   48,     2,  4608,  1867>,
        block_fft_implementation<48,   48,    6,     4,  4608,  1869>
    >;
};

template<> struct block_fft_record<300, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<30,   30,   10,     3,  2400,  1870>,
        block_fft_implementation<30,   30,   10,     3,  4800,  1872>,
        block_fft_implementation<60,   60,    5,    25,  2400,  1871>,
        block_fft_implementation<60,   60,    5,    24,  4800,  1873>
    >;
};

template<> struct block_fft_record<304, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<38,   38,    8,     4,  2432,  1874>,
        block_fft_implementation<38,   38,    8,     4,  4864,  1875>
    >;
};

template<> struct block_fft_record<320, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<40,   40,    8,     4,  2560,  1877>,
        block_fft_implementation<20,   20,   16,     2,  2560,  1876>,
        block_fft_implementation<20,   20,   16,     2,  5120,  1878>,
        block_fft_implementation<40,   40,    8,     8,  5120,  1881>,
        block_fft_implementation<10,   10,   32,     1,  5120,  1879>,
        block_fft_implementation<10,   10,   32,     2,  2560,  1880>
    >;
};

template<> struct block_fft_record<336, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,    8,     4,  2688,  1882>,
        block_fft_implementation<42,   42,    8,     4,  5376,  1883>
    >;
};

template<> struct block_fft_record<352, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<44,   44,    8,     8,  2816,  1884>,
        block_fft_implementation<22,   22,   16,     2,  2816,  1886>,
        block_fft_implementation<22,   22,   16,     2,  5632,  1885>,
        block_fft_implementation<44,   44,    8,     4,  5632,  1887>
    >;
};

template<> struct block_fft_record<360, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    6,    21,  2880,  1889>,
        block_fft_implementation<30,   30,   12,     5,  2880,  1888>,
        block_fft_implementation<30,   30,   12,     5,  5760,  1890>,
        block_fft_implementation<60,   60,    6,    20,  5760,  1891>
    >;
};

template<> struct block_fft_record<368, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<46,   46,    8,     4,  2944,  1892>,
        block_fft_implementation<46,   46,    8,     4,  5888,  1893>
    >;
};

template<> struct block_fft_record<384, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<24,   24,   16,     2,  3072,  1895>,
        block_fft_implementation<12,   12,   32,     1,  3072,  1894>,
        block_fft_implementation<12,   12,   32,     1,  6144,  1896>,
        block_fft_implementation<48,   48,    8,     4,  3072,  1897>,
        block_fft_implementation<24,   24,   16,     2,  6144,  1898>,
        block_fft_implementation<48,   48,    8,     3,  6144,  1901>,
        block_fft_implementation< 6,    6,   64,     1,  6144,  1900>,
        block_fft_implementation< 6,    6,   64,     2,  3072,  1899>
    >;
};

template<> struct block_fft_record<392, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   14,     4,  3136,  1902>,
        block_fft_implementation<28,   28,   14,     2,  6272,  1905>,
        block_fft_implementation<14,   14,   28,     1,  3136,  1903>,
        block_fft_implementation<56,   56,    7,     9,  3136,  1906>,
        block_fft_implementation<14,   14,   28,     1,  6272,  1904>,
        block_fft_implementation<56,   56,    7,     8,  6272,  1907>
    >;
};

template<> struct block_fft_record<416, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<52,   52,    8,     8,  3328,  1908>,
        block_fft_implementation<26,   26,   16,     2,  6656,  1910>,
        block_fft_implementation<26,   26,   16,     2,  3328,  1909>,
        block_fft_implementation<52,   52,    8,     4,  6656,  1911>
    >;
};

template<> struct block_fft_record<432, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<36,   36,   12,     5,  3456,  1912>,
        block_fft_implementation<12,   12,   36,     3,  3456,  1913>,
        block_fft_implementation<36,   36,   12,     5,  6912,  1921>,
        block_fft_implementation< 6,    6,   72,     3,  3456,  1914>,
        block_fft_implementation<24,   24,   18,     3,  3456,  1915>,
        block_fft_implementation<12,   12,   36,     3,  6912,  1916>,
        block_fft_implementation<18,   18,   24,     5,  3456,  1917>,
        block_fft_implementation<18,   18,   24,     5,  6912,  1918>,
        block_fft_implementation<54,   54,    8,     8,  3456,  1922>,
        block_fft_implementation< 6,    6,   72,     7,  6912,  1919>,
        block_fft_implementation<24,   24,   18,     7,  6912,  1920>,
        block_fft_implementation<48,   48,    9,     7,  3456,  1923>,
        block_fft_implementation<54,   54,    8,    12,  6912,  1924>,
        block_fft_implementation<48,   48,    9,    24,  6912,  1925>
    >;
};

template<> struct block_fft_record<448, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<28,   28,   16,     2,  3584,  1926>,
        block_fft_implementation<56,   56,    8,     4,  3584,  1927>,
        block_fft_implementation<28,   28,   16,     2,  7168,  1928>,
        block_fft_implementation<14,   14,   32,     1,  7168,  1929>,
        block_fft_implementation<14,   14,   32,     2,  3584,  1930>,
        block_fft_implementation<56,   56,    8,     8,  7168,  1931>
    >;
};

template<> struct block_fft_record<464, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<58,   58,    8,     4,  3712,  1932>,
        block_fft_implementation<58,   58,    8,     8,  7424,  1933>
    >;
};

template<> struct block_fft_record<480, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<60,   60,    8,     4,  3840,  1935>,
        block_fft_implementation<30,   30,   16,     2,  3840,  1934>,
        block_fft_implementation<30,   30,   16,     2,  7680,  1936>,
        block_fft_implementation<60,   60,    8,     8,  7680,  1937>
    >;
};

template<> struct block_fft_record<496, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<62,   62,    8,     4,  3968,  1938>,
        block_fft_implementation<62,   62,    8,     8,  7936,  1939>
    >;
};

template<> struct block_fft_record<500, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<50,   50,   10,     3,  4000,  1941>,
        block_fft_implementation<10,   10,   50,     5,  4000,  1940>,
        block_fft_implementation<20,   20,   25,     5,  4000,  1942>,
        block_fft_implementation<10,   10,   50,     5,  8000,  1943>,
        block_fft_implementation<20,   20,   25,     5,  8000,  1944>,
        block_fft_implementation<50,   50,   10,    16,  8000,  1945>
    >;
};

template<> struct block_fft_record<504, double, fft_type::c2c, fft_direction::inverse, 900> {
    static constexpr bool defined = true;
    using blobs = type_list<
        block_fft_implementation<42,   42,   12,     5,  4032,  1946>,
        block_fft_implementation<42,   42,   12,     2,  8064,  1947>
    >;
};
