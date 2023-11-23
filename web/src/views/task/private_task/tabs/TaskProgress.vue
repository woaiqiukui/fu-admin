<template>
  <div class="pt-4 m-4 desc-wrap">
    <a-card title="任务进度" :bordered="false">
      <a-steps :current="1" progress-dot size="small">
        <a-step title="创建项目">
          <template #description>
            <div>
              {{ project_name }}
            </div>
            <p>{{ task_create_time }}</p>
          </template>
        </a-step>
        <a-step title="端口扫描">
          <template #description>
            <p v-if="port_result.length > 0">
              <span v-for="(port, index) in port_result" :key="index">
                {{ port.port }}{{ index < port_result.length - 1 ? ', ' : '' }}
              </span>
            </p>
            <p v-else>No ports scanned</p>
          </template>
        </a-step>
        <a-step title="漏洞扫描">
          <template #description>
            <p>已完成</p>
          </template>
        </a-step>
        <a-step title="完成" />
      </a-steps>
    </a-card>

    <a-card title="任务信息" :boardred="false" class="mt-5">
      <a-descriptions column="3">
        <a-descriptions-item label="任务名称">{{ task_name }}</a-descriptions-item>
        <a-descriptions-item label="任务创建时间">{{ task_create_time }}</a-descriptions-item>
        <a-descriptions-item label="端口列表">
          <span v-if="port_result.length > 0">
            <span v-for="(port, index) in port_result" :key="index">
              {{ port.port }}{{ index < port_result.length - 1 ? ', ' : '' }}
            </span>
          </span>
          <span v-else>No ports scanned</span>
        </a-descriptions-item>
        <a-descriptions-item label="漏洞数量">2131</a-descriptions-item>
      </a-descriptions>
    </a-card>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { toRefs } from '@vueuse/core';
  import { Divider, Card, Descriptions, Steps, Tabs } from 'ant-design-vue';

  export default defineComponent({
    name: 'TaskProgress',
    components: {
      [Divider.name]: Divider,
      [Card.name]: Card,
      [Descriptions.name]: Descriptions,
      [Descriptions.Item.name]: Descriptions.Item,
      [Steps.name]: Steps,
      [Steps.Step.name]: Steps.Step,
      [Tabs.name]: Tabs,
      [Tabs.TabPane.name]: Tabs.TabPane,
    },
    props: {
      project_name: String,
      task_create_time: Date,
      port_result: Array,
      task_name: String,
    },
    setup(props) {
      const { project_name, task_create_time, port_result, task_name } = toRefs(props);

      return {};
    },
  });
</script>
