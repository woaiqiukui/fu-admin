<template>
  <PageWrapper title="安全漏洞推送">
    <a-card>
      <VulnerabilityInfo :vulnerabilities="vulnerabilities" />
    </a-card>
  </PageWrapper>
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Divider, Card, Descriptions, Steps, Tabs } from 'ant-design-vue';
  import VulnerabilityInfo from './VulnerabilityInfo.vue'; // Import your component
  import { getList } from './api'; // Import your API function

  export default defineComponent({
    name: 'WatchVuln',
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
      VulnerabilityInfo,
    },
    setup() {
      const vulnerabilities = ref([]);

      // Fetch data from the API
      const fetchData = async () => {
        try {
          // Make the API request to get vulnerability data
          const response = await getList(); // Assuming getList is imported
          vulnerabilities.value = response;
          console.log(vulnerabilities.value);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };

      // Fetch data on component mount
      onMounted(() => {
        fetchData();
      });

      return { vulnerabilities };
    },
  });
</script>
