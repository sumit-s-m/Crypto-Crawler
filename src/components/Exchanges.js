import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import millify from 'millify';
import { Collapse, Row, Col, Typography, Avatar, Card, Statistic } from 'antd';
import HTMLReactParser from 'html-react-parser';
import { useGetCryptoDetailsQuery, useGetCryptosQuery,useGetCryptoHistoryQuery } from '../services/cryptoAPI';
import { MoneyCollectOutlined, DollarCircleOutlined, FundOutlined, ExclamationCircleOutlined, StopOutlined, TrophyOutlined, CheckOutlined, NumberOutlined, ThunderboltOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;
// const { Option } = Select; 

function Exchanges() {
  const count = 100;
  const { data: cryptosList, isFetching } = useGetCryptosQuery(count);
  const [cryptos, setCryptos] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [hoveredCoin, setHoveredCoin] = useState(null);
  const { coinId } = useParams();
  const { data } = useGetCryptoDetailsQuery(coinId);
  const cryptoDetails = data?.data?.coin ?? {};
  const [timeperiod, setTimeperiod] = useState('7d');
  const { data: coinHistory } = useGetCryptoHistoryQuery({coinId,timeperiod});


  useEffect(() => {
    const filteredData = cryptosList?.data?.coins.filter((item) => item.name.toLowerCase().includes(searchTerm)) ?? [];
    setCryptos(filteredData);
  }, [cryptosList, searchTerm])

  if (isFetching) return 'Loading...';

  if (!cryptoDetails) return null;

  const handleCoinHover = (coin) => {
    setHoveredCoin(coin);
  };

  const handleCoinLeave = () => {
    setHoveredCoin(null);
  };

  const stats = [
    { title: 'Number Of Exchanges', value: cryptoDetails.numberOfExchanges, icon: <MoneyCollectOutlined /> },
    { title: '24h Volume', value: `$ ${cryptoDetails?.["24hVolume"] && millify(cryptoDetails?.["24hVolume"])}`, icon: <ThunderboltOutlined /> },
    { title: 'Number Of Markets', value: cryptoDetails.numberOfMarkets, icon: <FundOutlined /> },
    { title: 'Market Cap', value: `$ ${cryptoDetails.marketCap && millify(cryptoDetails.marketCap)}`, icon: <DollarCircleOutlined /> },
  ];

  return (
    <>
      <Row>
        <Col span={4}></Col>
        <Col span={5}>Symbol</Col>
        <Col span={5}>Price</Col>
        <Col span={5}>Markets</Col>
        <Col span={5}>Change</Col>
      </Row>
      <Row gutter={[32, 8]}>
        {cryptos && cryptos.map((currency) => {
          const isHovered = currency.uuid === hoveredCoin;
          return (
            <Col xs={24} sm={32} lg={32} className="crypto-card" key={currency.uuid}>
              <Card
                title={`${currency.rank}. ${currency.name}`}
                extra={<img className="crypto-image" src={currency.iconUrl} />}
                hoverable
                onMouseEnter={() => handleCoinHover(currency.uuid)}
                onMouseLeave={handleCoinLeave}
              >
                <Row>
                  <Col span={4}></Col>
                  <Col span={4}>{millify(currency.symbol)}</Col>
                  <Col span={5}>{millify(currency.price)}</Col>
                  <Col span={5}>{millify(currency.marketCap)}</Col>
                  <Col span={5}>{millify(currency.change)}%</Col>
                </Row>
              
              </Card>
            </Col>
          );
        })}
      </Row>
    </>
  );
}

export default Exchanges;
