<template>
  <div class="step1">
    <div class="step1-form">
      <BasicForm @register="register" />
    </div>
    <a-divider />
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicForm, useForm } from '/@/components/Form';
  import { step1Schemas } from './data';
  import { getList as getProjectList } from '../project/api';
  import { Divider } from 'ant-design-vue';
  import { useModalInner } from '/@/components/Modal';

  export default defineComponent({
    components: {
      BasicForm,
      [Divider.name]: Divider,
    },
    emits: ['next'],
    setup(_, { emit }) {
      const isUpdate = ref(true);

      const [register, { resetFields, setFieldsValue, updateSchema, validate }] = useForm({
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

      const [registerModal, { setModalProps }] = useModalInner(async (data) => {
        resetFields();
        setModalProps({ confirmLoading: false });
        isUpdate.value = !!data?.isUpdate;

        if (unref(isUpdate)) {
          setFieldsValue({
            ...data.record,
          });
        }
        // 获取项目列表并更新下拉框选项
        const projectList = await getProjectList();
        console.log(projectList);
        const projectOptions = projectList.items.map((project) => ({
          label: project.project_name,
          value: project.id,
        }));
        updateSchema({
          field: 'project',
          componentProps: { options: projectOptions },
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
        register,
        registerModal,
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
