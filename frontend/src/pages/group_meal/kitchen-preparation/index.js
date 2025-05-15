import React, { useState, useEffect } from 'react';
import { Table, Card, message, Drawer, Spin } from 'antd';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import PreparationDetail from './components/PreparationDetail';

const KitchenPreparation = () => {
  const [loading, setLoading] = useState(false);
  const [preparations, setPreparations] = useState([]);
  const [selectedPreparation, setSelectedPreparation] = useState(null);
  const [drawerVisible, setDrawerVisible] = useState(false);
  const { hotelId } = useParams();

  // 表格列定义
  const columns = [
    {
      title: '宴会名称',
      dataIndex: 'event_name',
      key: 'event_name',
      render: (text) => text || '未命名宴会',
    },
    {
      title: '日期',
      dataIndex: 'event_date',
      key: 'event_date',
      sorter: (a, b) => new Date(a.event_date) - new Date(b.event_date),
    },
    {
      title: '时间',
      dataIndex: 'event_time',
      key: 'event_time',
    },
    {
      title: '人数',
      dataIndex: 'guest_count',
      key: 'guest_count',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => {
        const statusMap = {
          'pending': '待处理',
          'in_progress': '进行中',
          'completed': '已完成',
          'cancelled': '已取消'
        };
        return statusMap[status] || status;
      }
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress) => `${progress}%`
    }
  ];

  // 获取准备任务列表
  const fetchPreparations = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/kitchen-prep/${hotelId}/preparations`);
      if (response.data && response.data.preparations) {
        setPreparations(response.data.preparations);
      }
    } catch (error) {
      message.error('获取厨房准备任务列表失败');
      console.error('Error fetching preparations:', error);
    } finally {
      setLoading(false);
    }
  };

  // 获取准备任务详情
  const fetchPreparationDetail = async (preparationId) => {
    try {
      const response = await axios.get(`/api/kitchen-prep/${hotelId}/preparations/${preparationId}`);
      if (response.data && response.data.preparation) {
        setSelectedPreparation(response.data.preparation);
        setDrawerVisible(true);
      }
    } catch (error) {
      message.error('获取准备任务详情失败');
      console.error('Error fetching preparation detail:', error);
    }
  };

  useEffect(() => {
    fetchPreparations();
  }, [hotelId]);

  // 处理行点击事件
  const handleRowClick = (record) => {
    fetchPreparationDetail(record.id);
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card title="厨房准备任务列表">
        <Spin spinning={loading}>
          <Table
            columns={columns}
            dataSource={preparations}
            rowKey="id"
            onRow={(record) => ({
              onClick: () => handleRowClick(record)
            })}
          />
        </Spin>
      </Card>

      <Drawer
        title="准备任务详情"
        placement="right"
        width={720}
        onClose={() => {
          setDrawerVisible(false);
          setSelectedPreparation(null);
        }}
        visible={drawerVisible}
      >
        {selectedPreparation && (
          <PreparationDetail
            preparation={selectedPreparation}
            onStatusChange={() => fetchPreparations()}
          />
        )}
      </Drawer>
    </div>
  );
};

export default KitchenPreparation;