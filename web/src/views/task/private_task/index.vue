<template>
  <PageWrapper title="项目名称" contentBackground>
    <template #extra>
      <a-button> 操作二 </a-button>
      <a-button type="primary"> 主操作 </a-button>
    </template>

    <template #footer>
      <a-tabs type="card" default-active-key="1">
        <a-tab-pane key="1" tab="任务情况汇总"> <TaskProgress /> </a-tab-pane>
        <a-tab-pane key="2" tab="端口信息"> <PortPage /> </a-tab-pane>
        <a-tab-pane key="3" tab="服务信息"> <PortPage /> </a-tab-pane>
        <a-tab-pane key="4" tab="指纹信息"> <PortPage /> </a-tab-pane>
        <a-tab-pane key="5" tab="弱口令信息"> <PortPage /> </a-tab-pane>
        <a-tab-pane key="6" tab="漏洞信息"> <PortPage /> </a-tab-pane>
      </a-tabs>
    </template>
  </PageWrapper>
</template>
<script lang="ts">
  import TaskProgress from './tabs/TaskProgress.vue';
  import PortPage from './tabs/Port.vue';
  import { defineComponent } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Divider, Card, Descriptions, Steps, Tabs } from 'ant-design-vue';

  export default defineComponent({
    name: 'PrivateTaskManagment',
    components: {
      PageWrapper,
      [Divider.name]: Divider,
      [Card.name]: Card,
      [Descriptions.name]: Descriptions,
      [Descriptions.Item.name]: Descriptions.Item,
      [Steps.name]: Steps,
      [Steps.Step.name]: Steps.Step,
      [Tabs.name]: Tabs,
      [Tabs.TabPane.name]: Tabs.TabPane,
      TaskProgress,
      PortPage,
    },
    setup() {
      return {};
    },
  });
</script>
