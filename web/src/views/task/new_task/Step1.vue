<template>
  <div class="step1">
    <div class="step1-form">
      <BasicForm @register="register" />
      <a-button type="primary" @click="customSubmitFunc">下一步</a-button>
    </div>
    <a-divider />
  </div>
</template>
<script lang="ts">
  import { defineComponent, onMounted } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { step1Schemas, getProjectOptions } from './data';
  import { Divider } from 'ant-design-vue';

  export default defineComponent({
    components: {
      BasicForm,
      [Divider.name]: Divider,
    },
    emits: ['next'],
    setup(_, { emit }) {
      onMounted(async () => {
        await getProjectOptions();
      });

      const [register, { validate }] = useForm({
        labelWidth: 100,
        schemas: step1Schemas,
        actionColOptions: {
          span: 14,
        },
        showResetButton: false,
        submitButtonOptions: {
          text: '下一步',
        },
        submitFunc: customSubmitFunc,
      });

      async function customSubmitFunc() {
        try {
          const values = await validate();
          emit('next', values);
        } catch (error) {
          console.log(error);
        }
      }

      return {
        register,
        customSubmitFunc,
      };
    },
  });
</script>
<style lang="less" scoped>
  .step1 {
    &-form {
      width: 450px;
      margin: 0 auto;
    }

    h3 {
      margin: 0 0 12px;
      color: @text-color;
      font-size: 16px;
      line-height: 32px;
    }

    h4 {
      margin: 0 0 4px;
      color: @text-color;
      font-size: 14px;
      line-height: 22px;
    }

    p {
      color: @text-color;
    }
  }
</style>
