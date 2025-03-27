#include <iostream>
#include <nvapi.h>

#pragma comment(lib, "nvapi64.lib")  // Link to NVAPI library

int main() {
    // Initialize NVAPI
    NvAPI_Status status = NvAPI_Initialize();
    if (status != NVAPI_OK) {
        std::cerr << "Failed to initialize NVAPI" << std::endl;
        return -1;
    }

    // Get the handle to the first GPU (0-indexed)
    NvPhysicalGpuHandle gpuHandle;
    status = NvAPI_GPU_GetPhysicalGPUs(&gpuHandle, 1);
    if (status != NVAPI_OK) {
        std::cerr << "Failed to get GPU handle" << std::endl;
        NvAPI_Unload();
        return -1;
    }

    // Query the current memory clock (for monitoring purposes)
    NvU32 currentMemClock;
    status = NvAPI_GPU_GetMemoryClock(gpuHandle, &currentMemClock);
    if (status != NVAPI_OK) {
        std::cerr << "Failed to get memory clock" << std::endl;
        NvAPI_Unload();
        return -1;
    }

    std::cout << "Current Memory Clock: " << currentMemClock << " MHz" << std::endl;

    // Set the memory clock to a new value (e.g., +500 MHz)
    NvU32 newMemClock = currentMemClock + 0;  // Add 500 MHz offset
    status = NvAPI_GPU_SetMemoryClock(gpuHandle, newMemClock);

    if (status == NVAPI_OK) {
        std::cout << "Memory Clock successfully set to: " << newMemClock << " MHz" << std::endl;
    } else {
        std::cerr << "Failed to set memory clock" << std::endl;
    }

    // Clean up NVAPI
    NvAPI_Unload();
    return 0;
}