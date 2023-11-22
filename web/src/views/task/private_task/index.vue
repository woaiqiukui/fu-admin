<template>
  <PageWrapper :title="project_name" contentBackground>
    <template #extra>
      <a-button v-for="task in task_list_name_and_uuid" :key="task.uuid">
        {{ task.task_name }}
      </a-button>
      <a-button type="primary"> {{ task_name }} </a-button>
    </template>

    <template #footer>
      <a-tabs type="card" default-active-key="1">
        <a-tab-pane key="1" tab="任务情况汇总">
          <TaskProgress :task_uuid="task_uuid" />
        </a-tab-pane>
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
  import { Ref, defineComponent, onMounted, ref, watch } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Divider, Card, Descriptions, Steps, Tabs } from 'ant-design-vue';
  import { useRoute } from 'vue-router';
  import { getTaskResult } from './api';

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
      const route = useRoute();
      const task_uuid = ref<string>('');

      interface TaskResultItem {
        uuid: string;
        creator_id: number;
        modifier: string;
        update_datetime: Date;
        create_datetime: Date;
        sort: number;
        task_name: string;
        project_uuid_id: string;
        task_desc: string;
        task_type: string;
        task_status: string;
        public_full_company_name_input: string;
        public_root_domain_input: string;
        public_ip_input: string;
        public_domain_brute_force: boolean;
        public_historical_domain_query: boolean;
        public_port_scanning: boolean;
        public_fingerprint_identification: boolean;
        public_fofa: boolean;
        public_hunter: boolean;
        public_quake: boolean;
        private_ip_input: string;
        private_port_scanning: string;
        private_default_ports_input: string;
        private_custom_ports_input: string;
        private_fingerprint_identification: boolean;
        private_weak_password_detection: boolean;
        private_poc_scanning: boolean;
      }

      const project_name = ref('');
      const task_list_name_and_uuid: Ref<{ task_name: string; uuid: string }[]> = ref([]);
      const port_result = ref([]);
      const task_result: Ref<TaskResultItem[]> = ref([]);

      const task_create_time: Ref<Date | null> = ref(null);
      const task_name = ref('');

      const fetchData = async () => {
        if (task_uuid.value) {
          const taskResult = await getTaskResult(task_uuid.value);
          if (taskResult) {
            project_name.value = taskResult.project_name;
            // 展示该项目下所有其他任务
            task_list_name_and_uuid.value = taskResult.task_list_name_and_uuid.filter(
              (task) => task.uuid !== task_uuid.value,
            );
            port_result.value = taskResult.port_result;
            task_result.value = taskResult.task_result;
            task_create_time.value =
              task_result.value.length > 0 ? task_result.value[0].update_datetime : null;
            task_name.value = task_result.value.length > 0 ? task_result.value[0].task_name : '';
          }
        }
      };

      watch(
        () => task_uuid.value,
        (newValue) => {
          if (newValue) {
            fetchData();
          }
        },
        { immediate: true },
      );

      onMounted(() => {
        if (Array.isArray(route.params.task_uuid)) {
          task_uuid.value = route.params.task_uuid[0];
        } else {
          task_uuid.value = route.params.task_uuid;
        }
        // fetchData();
      });

      return {
        project_name,
        task_uuid,
        task_name,
        task_list_name_and_uuid,
      };
    },
  });
</script>
