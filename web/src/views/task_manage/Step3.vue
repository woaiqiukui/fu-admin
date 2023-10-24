<template>
  <div class="step1">
    <div class="step1-form">
      <BasicForm @register="register">
        <template #fac="{ model, field }">
          <a-input-group compact>
            <a-select v-model="model[TaskType]" class="TaskType-select">
              <a-select-option value="1">公网资产监控</a-select-option>
              <a-select-option value="2">内网资产扫描</a-select-option>
            </a-select>
          </a-input-group>
        </template>
      </BasicForm>
    </div>
    <a-driver />
  </div>
</template>
<script lang="ts">
    import { defineComponent } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { step1Schemas } from './data';

  import { Select, Input, Divider } from 'ant-design-vue';
  import { custom } from 'vue-types';

  export default defineComponent({
    components: {
      BasicForm,
      [Select.name]: Select,
      ASelectOption: Select.Option,
      [Input.name]: Input,
      [Input.Group.name]: Input.Group,
      [Divider.name]: Divider,
    },
    emits: ['next'],
    setup(_, { emit }) {
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
          // console.log(error);
        }
      }

      return {
        register,
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

  .pay-select {
    width: 20%;
  }

  .pay-input {
    width: 70%;
  }
</style>
