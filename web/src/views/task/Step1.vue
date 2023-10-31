<template>
  <BasicModal v-bind="$attrs" @register="registerModal">
    <BasicForm @register="registerForm" />
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { step1Schemas } from './data';
  import { getList as getProjectList } from '../project/api';
  import { Divider } from 'ant-design-vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';

  export default defineComponent({
    name: 'Step1',
    components: {
      BasicModal,
      BasicForm,
      [Divider.name]: Divider,
    },
    emits: ['next'],
    setup(_, { emit }) {
      const isUpdate = ref(true);

      const [registerForm, { resetFields, setFieldsValue, updateSchema, validate }] = useForm({
        labelWidth: 100,
        baseColProps: { span: 24 },
        schemas: step1Schemas,
        showActionButtonGroup: false,
      });

      const [registerModal, { setModalProps }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;

        if (unref(isUpdate)) {
          setFieldsValue({
            ...data.record,
          });
        }
        const projectData = await getProjectList();
        updateSchema({
          field: 'project',
          componentProps: { projectData },
        });
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
        registerModal,
        registerForm,
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

  .pay-select {
    width: 20%;
  }

  .pay-input {
    width: 70%;
  }
</style>
