<template>
  <div class="step2">
    <a-alert v-if="stepValue.task_type === '1'" message="正在创建公网资产监控任务。" show-icon />
    <a-alert
      v-else-if="stepValue.task_type === '2'"
      message="正在创建内网资产扫描任务。"
      show-icon
    />
    <a-descriptions :column="1" class="mt-5">
      <a-descriptions-item label="任务名称"> {{ stepValue.task_name }} </a-descriptions-item>
      <a-descriptions-item label="任务描述"> {{ stepValue.task_desc }} </a-descriptions-item>
    </a-descriptions>
    <BasicForm @register="registerForm" />
    <a-divider />
    <a-button type="link" @click="customResetFunc">上一步</a-button>
    <a-button type="primary" @click="customSubmitFunc">完成</a-button>
  </div>
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { Alert, Divider, Descriptions } from 'ant-design-vue';
  import { publicSchemas, privateSchemas } from './data';
  import { createOrUpdate } from './api';

  export default defineComponent({
    components: {
      BasicForm,
      [Alert.name]: Alert,
      [Divider.name]: Divider,
      [Descriptions.name]: Descriptions,
      [Descriptions.Item.name]: Descriptions.Item,
    },
    // eslint-disable-next-line vue/require-prop-types
    props: {
      step1Values: {
        type: Object,
        required: true,
      },
    },
    emits: ['next', 'prev'],
    setup(props, { emit }) {
      // eslint-disable-next-line vue/no-setup-props-destructure
      const stepValue = props.step1Values;
      let schemasValue = publicSchemas;
      if (stepValue.task_type == 2) {
        schemasValue = privateSchemas;
      }

      const [registerForm, { validate, setProps }] = useForm({
        labelWidth: 80,
        schemas: schemasValue,
        actionColOptions: {
          span: 14,
        },
        resetButtonOptions: {
          text: '上一步',
        },
        submitButtonOptions: {
          text: '提交',
        },
        resetFunc: customResetFunc,
        submitFunc: customSubmitFunc,
      });

      async function customResetFunc() {
        emit('prev');
      }

      async function customSubmitFunc() {
        try {
          const values = await validate();

          const taskValues = {
            ...stepValue,
            ...values,
          };
          const result = await createOrUpdate(taskValues, false);

          setProps({
            submitButtonOptions: {
              loading: true,
            },
          });
          setTimeout(() => {
            setProps({
              submitButtonOptions: {
                loading: false,
              },
            });
            emit('next', values, result);
          }, 1500);
        } catch (error) {}
      }

      return {
        stepValue,
        registerForm,
        customResetFunc,
        customSubmitFunc,
      };
    },
  });
</script>
<style lang="less" scoped>
  .step2 {
    width: 500px;
    margin: 0 auto;
  }
</style>
