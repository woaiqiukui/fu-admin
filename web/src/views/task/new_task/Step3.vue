<template>
  <div class="step3">
    <a-result status="success" title="任务创建成功">
      <template #extra>
        <a-button type="primary" @click="redo"> 创建新任务 </a-button>
        <a-button @click="navigateToTask(task_uuid)"> 查看任务详情 </a-button>
      </template>
    </a-result>
    <div class="desc-wrap">
      <a-descriptions :column="1" class="mt-5">
        <a-descriptions-item label="任务名称"> {{ stepValue1.task_name }} </a-descriptions-item>
        <a-descriptions-item label="任务描述"> {{ stepValue1.task_desc }} </a-descriptions-item>
        <a-descriptions-item label="任务目标" style="white-space: pre-wrap">
          {{
            (stepValue2.full_company_name_input
              ? '公司全称：\n' + stepValue2.full_company_name_input + '\n'
              : '') +
            (stepValue2.root_domain_input
              ? '根域名列表：\n' + stepValue2.root_domain_input + '\n'
              : '') +
            (stepValue2.ip_input ? 'IP 列表：\n' + stepValue2.ip_input : '')
          }}
        </a-descriptions-item>
      </a-descriptions>
    </div>
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { Result, Descriptions } from 'ant-design-vue';
  import { router } from '/@/router';

  export default defineComponent({
    components: {
      [Result.name]: Result,
      [Descriptions.name]: Descriptions,
      [Descriptions.Item.name]: Descriptions.Item,
    },
    props: {
      step1Values: {
        type: Object,
        required: true,
      },
      step2Values: {
        type: Object,
        required: true,
      },
      result: {
        type: Object,
        required: true,
      },
    },
    emits: ['redo'],
    setup(props, { emit }) {
      // eslint-disable-next-line vue/no-setup-props-destructure
      const stepValue1 = props.step1Values;
      // eslint-disable-next-line vue/no-setup-props-destructure
      const stepValue2 = props.step2Values;

      // eslint-disable-next-line vue/no-setup-props-destructure
      const task_uuid = props.result.uuid;
      const navigateToTask = (taskUuid) => {
        console.log(stepValue1);
        router.push(`/task/private_task/${taskUuid}`);
      };
      return {
        redo: () => {
          emit('redo');
        },
        stepValue1,
        stepValue2,
        task_uuid,
        navigateToTask,
      };
    },
  });
</script>
<style lang="less" scoped>
  .step3 {
    width: 600px;
    margin: 0 auto;
  }

  .desc-wrap {
    margin-top: 24px;
    padding: 24px 40px;
    background-color: @background-color-light;
  }
</style>
