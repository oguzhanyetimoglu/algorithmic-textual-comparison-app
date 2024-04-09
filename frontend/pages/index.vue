<template>
    <div class="container mx-auto mt-8">
        <h1 class="text-3xl font-bold mb-4">Welcome, {{ data.username }}!</h1>
        <p class="text-xl mb-8">We're glad to have you here.</p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Card 1 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center">Amount of all documents:</h2>
                <p class="text-4xl font-bold text-center">{{ totalDocuments }}</p>
            </div>

            <!-- Card 2 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center">Documents by Type</h2>
                <Piechart v-if="Object.keys(documentCounts).length > 0" :labels="Object.keys(documentCounts)"
                    :data="Object.values(documentCounts)" canvasId="pieChart1" />
            </div>

            <!-- Card 3 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center"># of Docs per 1st Digit of SIC:</h2>
                <Piechart v-if="Object.keys(tenKsWithSicCount).length > 0" :labels="Object.keys(tenKsWithSicCount)"
                    :data="Object.values(tenKsWithSicCount)" canvasId="pieChart2" />
            </div>

            <!-- Card 4 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center">Document Amount by State:</h2>
                <Piechart v-if="Object.keys(documentWithState).length > 0" :labels="Object.keys(documentWithState)"
                    :data="Object.values(documentWithState)" canvasId="pieChart3" />
            </div>

            <!-- Card 5 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center">Document Amount per Year:</h2>
                <Piechart v-if="Object.keys(documentPerYear).length > 0" :labels="Object.keys(documentPerYear)"
                    :data="Object.values(documentPerYear)" canvasId="pieChart4" />
            </div>

            <!-- Card 6 -->
            <div class="bg-white p-4 rounded-md shadow-md">
                <h2 class="text-xl font-bold mb-2 text-center">Document Amount per Month:</h2>
                <Piechart v-if="Object.keys(documentPerMonth).length > 0" :labels="Object.keys(documentPerMonth)"
                    :data="Object.values(documentPerMonth)" canvasId="pieChart5" />
            </div>
        </div>
    </div>
</template>

<script>

export default {

    data() {
        return {
            config: useRuntimeConfig(),
            totalDocuments: 0,
            tenKsWithSicCount: {},
            documentCounts: {},
            documentWithState: {},
            documentPerYear: {},
            documentPerMonth: {},
        };
    },

    setup() {
        const { data, status, signOut, token } = useAuth();

        return {
            data,
            status,
            signOut,
            token,
        };
    },
    async mounted() {
        const [totalDocuments, documentCounts, tenKsWithSicCount, documentWithState, documentPerYear, documentPerMonth] = await Promise.all([
            this.allDocuments(),
            this.documentTypes(),
            this.tenKsWithSic(),
            this.documentsWithState(),
            this.documentsPerYear(),
            this.documentsPerMonth(),
            // other function calls...
        ]);
        this.totalDocuments = totalDocuments;
        this.documentCounts = documentCounts;
        this.tenKsWithSicCount = tenKsWithSicCount;
        this.documentWithState = documentWithState;
        this.documentPerYear = documentPerYear;
        this.documentPerMonth = documentPerMonth;
    },
    methods: {
        async getCount(url) {
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data);
                return data.count;
            } catch (error) {
                console.error(error);
                return 0;
            }
        },
        async allDocuments() {
            let url = `${this.config.public.apiBase}/api/ten-k/?count_only=true`;
            return await this.getCount(url);
        },
        async documentTypes() {
            let url = `${this.config.public.apiBase}/api/ten-k/?count_by_filing_type=true`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data);
                return data;
            } catch (error) {
                console.error(error);
                return {};
            }
        },
        async tenKsWithSic() {
            let counts = {};
            for (let i = 1; i <= 9; i++) {
                let url = `${this.config.public.apiBase}/api/ten-k/?sic_start=${i}&count_only=true`;
                counts[i] = await this.getCount(url);
            }
            return counts;
        },
        async documentsWithState() {
            let url = `${this.config.public.apiBase}/api/ten-k/?count_by_state=true`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data);
                return data;
            } catch (error) {
                console.error(error);
                return {};
            }
        },
        async documentsPerYear() {
            let url = `${this.config.public.apiBase}/api/ten-k/?count_by_year=true`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data);
                return data;
            } catch (error) {
                console.error(error);
                return {};
            }
        },
        async documentsPerMonth() {
            let url = `${this.config.public.apiBase}/api/ten-k/?count_by_month=true`;
            try {
                const response = await fetch(url);
                const data = await response.json();
                console.log(data);

                const monthNames = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ];

                const labeledData = {};
                for (const monthNumber in data) {
                    const monthName = monthNames[parseInt(monthNumber) - 1];
                    labeledData[monthName] = data[monthNumber];
                }

                return labeledData;
            } catch (error) {
                console.error(error);
                return {};
            }
        },
    },
}
</script>