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
  import { defineComponent, onMounted, ref, watch } from 'vue';
  import { getTaskResult } from '../api';

  export default defineComponent({
    name: 'TaskProgress',
    props: {
      task_uuid: String,
    },
    setup(props) {
      const project_name = ref('');
      const task_list_name_and_uuid = ref([]);
      const port_result = ref([]);
      const task_result = ref([]);
      const task_create_time = ref('');
      const task_name = ref('');

      const fetchData = async () => {
        if (props.task_uuid) {
          const taskResult = await getTaskResult(props.task_uuid);
          if (taskResult && taskResult.data) {
            project_name.value = taskResult.data.project_name;
            task_list_name_and_uuid.value = taskResult.data.task_list_name_and_uuid;
            port_result.value = taskResult.data.port_result;
            task_result.value = taskResult.data.task_result;

            task_create_time.value =
              task_result.value.length > 0 ? task_result.value[0].update_datetime : '';
            task_name.value = task_result.value.length > 0 ? task_result.value[0].task_name : '';
          }
        }
      };

      watch(
        () => props.task_uuid,
        (newValue) => {
          if (newValue) {
            fetchData();
          }
        },
        { immediate: true },
      );

      onMounted(() => {
        fetchData();
      });

      return {
        project_name,
        task_create_time,
        port_result,
        task_name,
      };
    },
  });
</script>
