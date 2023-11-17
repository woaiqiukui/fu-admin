<template>
  <PageWrapper title="" contentBackground content="" contentClass="p-4">
    <div class="step-form-form">
      <a-steps :current="current">
        <a-step title="填写任务信息" />
        <a-step title="填写任务详情" />
        <a-step title="完成" />
      </a-steps>
    </div>
    <div class="mt-5">
      <Step1 @next="handleStep1Next" v-show="current === 0" />
      <Step2
        @prev="handleStepPrev"
        @next="handleStep2Next"
        v-show="current === 1"
        v-if="initSetp2"
        :step1Values="state.step1Values"
      />
      <Step3
        v-show="current === 2"
        @redo="handleRedo"
        v-if="initSetp3"
        :step1Values="state.step1Values"
        :step2Values="state.step2Values"
      />
    </div>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, ref, reactive, toRefs } from 'vue';
  import Step1 from './Step1.vue';
  import Step2 from './Step2.vue';
  import Step3 from './Step3.vue';
  import { PageWrapper } from '/@/components/Page';
  import { Steps } from 'ant-design-vue';

  export default defineComponent({
    name: 'NewTaskManagment',
    components: {
      Step1,
      Step2,
      Step3,
      PageWrapper,
      [Steps.name]: Steps,
      [Steps.Step.name]: Steps.Step,
    },
    setup() {
      const current = ref(0);

      const state = reactive({
        initSetp2: false,
        initSetp3: false,
        //保存 step1 的值
        step1Values: {},
        step2Values: {},
      });

      function handleStep1Next(step1Values: any) {
        current.value++;
        state.initSetp2 = true;
        console.log(step1Values);
        state.step1Values = step1Values;
      }

      function handleStepPrev() {
        state.initSetp2 = false;
        current.value--;
      }

      function handleStep2Next(step2Values: any) {
        current.value++;
        state.initSetp3 = true;
        console.log(step2Values);
        state.step2Values = step2Values;
        console.log(state.step1Values, state.step2Values);
      }

      function handleRedo() {
        current.value = 0;
        state.initSetp2 = false;
        state.initSetp3 = false;
      }

      return {
        current,
        state,
        handleStep1Next,
        handleStep2Next,
        handleRedo,
        handleStepPrev,
        ...toRefs(state),
      };
    },
  });
</script>
<style lang="less" scoped>
  .step-form-content {
    padding: 24px;
    background-color: @component-background;
  }

  .step-form-form {
    width: 750px;
    margin: 0 auto;
  }
</style>
