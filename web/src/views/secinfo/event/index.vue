<template>
  <PageWrapper title="安全资讯推送">
    <a-card>
      <SecInfoTable :secInfoList="secInfoList" />
    </a-card>
  </PageWrapper>
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Card } from 'ant-design-vue';
  import SecInfoTable from './SecInfo.vue'; // Import your SecInfo component
  import { getSecInfoList } from './api'; // Import your API function

  export default defineComponent({
    name: 'SecurityInformation',
    components: {
      PageWrapper,
      [Card.name]: Card,
      SecInfoTable,
    },
    setup() {
      const secInfoList = ref([]);

      // Fetch data from the API
      const fetchData = async () => {
        try {
          // Make the API request to get SecInfo data
          const response = await getSecInfoList(); // Assuming getSecInfoList is imported
          secInfoList.value = response;
          console.log(secInfoList.value);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };

      // Fetch data on component mount
      onMounted(() => {
        fetchData();
      });

      return { secInfoList };
    },
  });
</script>
