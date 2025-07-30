

#include <metal_stdlib>
using namespace metal;

kernel void noteTransform(device float* inData [[buffer(0)]],
                          device float* outData [[buffer(1)]],
                          uint id [[thread_position_in_grid]]) {
    float note = inData[id];
    // Add modulation using a sinusoidal pattern
    outData[id] = note + 2.0 * sin(note * 0.1);
}