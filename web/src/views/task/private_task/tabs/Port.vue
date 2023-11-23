<template>
  <a-table :columns="columns" :data-source="processedData" :row-selection="rowSelection" bordered />
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { Table } from 'ant-design-vue';

  export default defineComponent({
    name: 'PortPage',
    components: {
      [Table.name]: Table,
      [Table.Column.name]: Table.Column,
    },
    props: {
      portResult: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        columns: [
          {
            title: 'IP',
            dataIndex: 'ip',
            key: 'ip',
          },
          {
            title: '端口',
            dataIndex: 'port',
            key: 'port',
            width: '32%',
          },
          {
            title: 'Tag',
            dataIndex: 'tag',
            width: '30%',
            key: 'tag',
          },
        ],
        processedData: [],
        rowSelection: {}, // Add your rowSelection configuration if needed
      };
    },
    watch: {
      portResult: {
        handler(newVal) {
          // Process the data here to collapse IPs
          this.processedData = this.collapseIPs(newVal);
        },
        immediate: true,
      },
    },
    methods: {
      collapseIPs(data) {
        // Implement IP collapsing logic here
        // Example: Group data by IP
        const groupedByIP = data.reduce((acc, item) => {
          const key = item.ip;
          acc[key] = [...(acc[key] || []), item];
          return acc;
        }, {});

        // Process each group and collect results
        const processedData = Object.entries(groupedByIP).map(([ip, group]) => {
          // Sort group by port in ascending order
          group.sort((a, b) => a.port - b.port);

          // Transform the data structure for each IP group
          const transformedGroup = group.map((item, index) => ({
            key: index + 1,  // Use a numeric key for each item
            ip: item.ip,
            port: item.port,
            tag: item.tag,
            // Add more properties as needed
          }));

          // Return the processed data for each IP
          return {
            key: group[0].port,  // Use the smallest port as the key for the main group
            ip,
            port: group[0].port,  // Use the smallest port as the port for the main group
            tag: group[0].tag,    // Use the tag of the item with the smallest port
            // Add more properties as needed
            ...(transformedGroup.length > 0 && { children: transformedGroup }),  // Add children only if they exist
          };
        });

        console.log(processedData);
        return processedData;
      },
    },
  });
</script>
