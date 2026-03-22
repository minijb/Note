---
title: LipSync 共振峰方案
date: 2026-03-16
tags:
  - unity
  - lipsync
  - dots
  - job-system
  - algorithm
type: framework
aliases:
  - LipSync共振峰
  - 唇形同步共振峰
description: Unity 唇形同步技术方案，融合共振峰估计（F1/F2）与高斯相似度分类，结合 JobSystem 并行处理实现元音识别
draft: false
---

# LipSync 共振峰方案

下面给出一份综合之前两组改动（帧内归一化、帧间指数平滑、自适应能量阈值 + 基于共振峰 F1/F2 的分类与置信度回退机制）的完整修改方案。先简要说明每个文件修改要点，然后给出完整代码实现（各文件单独代码块）。
总体思路（要点）
在频谱平滑后做帧内归一化，减小整体能量波动对谱形判定的影响（NormalizeSpectrum）。
使用频谱能量 EMA 自适应判定静音阈值，丢弃低能量帧，减少误识别。
对每帧能量/置信度做帧间指数平滑，降低抖动（保存上一帧的 peak/置信度）。
增加基于共振峰（F1/F2）估计和 Gaussian 相似度分类，输出置信度；当置信度高时优先采用共振峰判定，否则回退到能量谱带方法。
使用 JobSystem 并行处理卷积、归一化、clarity 计算、能量法（并行每个元音）和 Formant 分类（IJob），并正确合并 JobHandle。
修改文件
Packages/com.hero.lipsync/Runtime/LipSync_Algo.cs：新增 EstimateFormants / ClassifyVowelByFormants（保留现有方法）。
Packages/com.hero.lipsync/Runtime/LipSync_Job.cs：新增 NormalizeSpectrum 与 FormantClassifyJob，保留并行 Convolute / Clarity / LipSyncJob。
Packages/com.hero.lipsync/Runtime/LipSync_JobEnv.cs：合并调度逻辑，加入 EMA 自适应阈值、帧间平滑、formant 输出与回退逻辑，正确分配/释放 NativeArray，并合并 JobHandles。
下面给出具体实现代码。
Packages/com.hero.lipsync/Runtime/LipSync_Algo.cs — 说明：在原有算法基础上加入共振峰估算与基于 F1/F2 的高斯相似度分类（返回索引与置信度），其余函数保持不变。



```csharp  
using System.Collections;  
using System.Collections.Generic;  
using Unity.Burst;  
using Unity.Collections;  
using Unity.Mathematics;  
using UnityEngine;  
  
namespace hero.LipSync.Runtime  
{  
    [BurstCompile]  
    public class LipSync_Algo  
    {  
        /// <summary>  
        ///  得到 spectrum 的能量和  
        /// </summary>  
        /// <param name="spectrum">频谱数据</param>  
        /// <returns>能量和</returns>  
        public static float GetSpectrumSum(NativeArray<float> spectrum)  
        {  
            float sum = 0.0f;  
            int len = spectrum.Length;  
            for (int i = 0; i < len; i++)  
            {  
                sum += spectrum[i];  
            }  
  
            return sum;  
        }  
  
        /// <summary>  
        ///  创建高斯滤波器  
        /// </summary>  
        public static NativeArray<float> GenerateGaussianFilter(int size, float deviationSquare)  
        {  
            NativeArray<float> result = new  NativeArray<float>(size, Allocator.Persistent);  
  
            float sum = 0.0f;  
            float mu = (float)(size - 1) / 2;  
            for (int i = 0; i < size; ++i)  
            {  
                float param = -((i - mu) * (i - mu)) / (2 * deviationSquare);  
                result[i] = math.exp(param);  
                sum += result[i];  
            }  
  
            for (int j = 0; j < size; ++j)  
            {  
                result[j] /= sum;  
            }  
  
            return result;  
        }  
  
        public static void Convolute(NativeArray<float> data, NativeArray<float> filter, EPaddleType type, NativeArray<float> output)  
        {  
            int filterMiddlePoint = Mathf.FloorToInt(filter.Length / 2.0f);  
            for (int n = 0; n < data.Length; n++)  
            {  
                output[n] = 0.0f;  
                for (int m = 0; m < filter.Length; m++)  
                {  
                    output[n] += GetValueFromArray(data, n - filterMiddlePoint + m, type) *  
                                 filter[filter.Length - m - 1];  
                }  
            }  
        }  
        public static void Convolute(NativeArray<float> data, NativeArray<float> filter, EPaddleType type, NativeArray<float> output, int filterMiddlePoint, int index)  
        {  
                output[index] = 0.0f;  
                for (int m = 0; m < filter.Length; m++)  
                {  
                    output[index] += GetValueFromArray(data, index - filterMiddlePoint + m, type) *  
                                 filter[filter.Length - m - 1];  
                }  
        }  
  
        /// <summary>  
        /// Find (length of peakvalue) local largest peak(s).        /// </summary>        /// <param name="data">Source data.</param>        /// <param name="peakValue">Array to store peak values.</param>        /// <param name="peakPosition">Array to store peak values' positions.</param>        public static void FindLocalLargestPeaks(NativeArray<float> data, NativeArray<float> peakValue, NativeArray<int> peakPosition)  
        {  
            int peakNum = 0;  
            float lastPeak = 0.0f;  
            int lastPeakPosition = 0;  
            bool isIncreasing = false;  
            bool isPeakIncreasing = false;  
  
            for (int i = 0; i < data.Length - 1; ++i)  
            {  
                if (data[i] < data[i + 1])  
                {  
                    isIncreasing = true;  
                }  
                else  
                {  
                    if (isIncreasing)  
                    {  
                        if (lastPeak < data[i]) // Peak found.  
                        {  
                            isPeakIncreasing = true;  
                        }  
                        else  
                        {  
                            if (isPeakIncreasing)  
                            {  
                                // Local largest peak found.  
                                peakValue[peakNum] = lastPeak;  
                                peakPosition[peakNum] = lastPeakPosition;  
                                ++peakNum;  
                            }  
  
                            isPeakIncreasing = false;  
                        }  
  
                        lastPeak = data[i];  
                        lastPeakPosition = i;  
                    }  
  
                    isIncreasing = false;  
                }  
  
                if (peakNum >= peakValue.Length)  
                {  
                    break;  
                }  
            }  
        }  
  
        public static float CalculateFrequencyBandRatio(NativeArray<float> spectrum, float lowFreq, float highFreq, float sampleRate)  
        {  
            int spectrumSize = spectrum.Length;  
  
            float nyquist = sampleRate / 2f;  
  
            // 计算频率对应的索引  
            int lowIndex = FrequencyToIndex(lowFreq, nyquist, spectrumSize);  
            int highIndex = FrequencyToIndex(highFreq, nyquist, spectrumSize);  
  
            float totalEnergy = 0f;  
            float targetBandEnergy = 0f;  
            for (int i = 0; i < spectrumSize; i++)  
            {  
                totalEnergy += spectrum[i] * spectrum[i];  
                if (i >= lowIndex && i <= highIndex)  
                    targetBandEnergy += spectrum[i] * spectrum[i];  
            }  
  
            if (totalEnergy <= 0f) return 0f;  
  
            return targetBandEnergy / totalEnergy;  
        }  
  
        public static int FrequencyToIndex(float frequency, float nyquist, int spectrumLength)  
        {  
            return (int)math.floor(frequency / nyquist * spectrumLength);  
        }  
  
        public static float GetFrequencyBandEnergy(NativeArray<float> spectrum, float minFreq, float maxFreq, float sampleRate)  
        {  
            int spectrumSize = spectrum.Length;  
            float totalEnergy = 0f;  
            int count = 0;  
  
            // 计算对应的频谱索引范围  
            int minIndex = (int)math.floor(minFreq * spectrumSize / (sampleRate / 2));  
            int maxIndex = (int)math.floor(maxFreq * spectrumSize / (sampleRate / 2));  
  
            minIndex = math.clamp(minIndex, 0, spectrumSize - 1);  
            maxIndex = math.clamp(maxIndex, 0, spectrumSize - 1);  
  
            // 使用对数加权累加频率带内的能量（语音频率感知更接近对数）  
            for (int i = minIndex; i <= maxIndex; i++)  
            {  
                // 使用更精细的频率权重，增强重要频率区域的影响  
                float frequency = i * (sampleRate / 2) / spectrumSize;  
                float weight = 1f;  
  
                // 对元音频率范围增加权重  
                if ((frequency >= 300 && frequency <= 1100) || // 低频元音  
                    (frequency >= 2000 && frequency <= 3000)) // 高频元音  
                {  
                    weight = 1.5f;  
                }  
  
                totalEnergy += spectrum[i] * weight;  
                count++;  
            }  
  
            return count > 0 ? totalEnergy / count : 0f;  
        }  
  
        public static float GetValueFromArray(NativeArray<float> data, int index, EPaddleType paddleType)  
        {  
            if (index >= 0 && index < data.Length)  
            {  
                return data[index];  
            }  
            else  
            {  
                switch (paddleType)  
                {  
                    case EPaddleType.Zero:  
                        return 0;  
                    case EPaddleType.Repeat:  
                        return index < 0 ? data[0] : data[data.Length - 1];  
                    case EPaddleType.Loop:  
                        int actualIndex = index;  
                        while (actualIndex < 0)  
                        {  
                            actualIndex += data.Length;  
                        }  
  
                        actualIndex %= data.Length;  
                        return data[actualIndex];  
                    default:  
                        return 0;  
                }  
            }  
        }  
  
        // --- 新增：共振峰估计（简化版） ---        // 估计谱图中的前两个局部峰（作为 F1, F2），返回频率（Hz）  
        public static void EstimateFormants(NativeArray<float> spectrum, int sampleRate, out float f1, out float f2)  
        {  
            f1 = 0f; f2 = 0f;  
            int n = spectrum.Length;  
            if (n < 3) return;  
  
            float top1Val = 0f, top2Val = 0f;  
            int top1Idx = -1, top2Idx = -1;  
            for (int i = 1; i < n - 1; i++)  
            {  
                if (spectrum[i] > spectrum[i - 1] && spectrum[i] > spectrum[i + 1])  
                {  
                    float v = spectrum[i] * spectrum[i];  
                    if (v > top1Val)  
                    {  
                        top2Val = top1Val; top2Idx = top1Idx;  
                        top1Val = v; top1Idx = i;  
                    }  
                    else if (v > top2Val)  
                    {  
                        top2Val = v; top2Idx = i;  
                    }  
                }  
            }  
  
            if (top1Idx >= 0)  
            {  
                float nyquist = sampleRate / 2f;  
                float freq1 = top1Idx * nyquist / n;  
                if (top2Idx >= 0)  
                {  
                    float freq2 = top2Idx * nyquist / n;  
                    if (freq1 <= freq2) { f1 = freq1; f2 = freq2; }  
                    else { f1 = freq2; f2 = freq1; }  
                }  
                else  
                {  
                    f1 = freq1; f2 = 0f;  
                }  
            }  
        }  
  
        // --- 新增：基于 F1/F2 的高斯相似度分类 ---        // 返回元音索引（0..4）与置信度（0..1），找不到或置信度极低则返回 -1        
        public static int ClassifyVowelByFormants(float f1, float f2, out float confidence)  
        {  
            confidence = 0f;  
            if (f1 <= 0f || f2 <= 0f) return -1;  
  
            // 参考均值 (F1, F2)（可在运行中微调）  
            float[,] means = new float[5, 2]  
            {  
                { 800f, 1200f }, // A  
                { 400f, 2000f }, // E  
                { 300f, 2400f }, // I  
                { 500f, 1000f }, // O  
                { 350f, 800f }   // U  
            };  
  
            float f1Sigma = 200f;  
            float f2Sigma = 400f;  
  
            float[] scores = new float[5];  
            float sum = 0f;  
            for (int i = 0; i < 5; i++)  
            {  
                float d1 = (f1 - means[i, 0]) / f1Sigma;  
                float d2 = (f2 - means[i, 1]) / f2Sigma;  
                float s = Mathf.Exp(-0.5f * (d1 * d1 + d2 * d2));  
                scores[i] = s;  
                sum += s;  
            }  
  
            if (sum <= 0f) return -1;  
  
            int best = -1;  
            float bestScore = 0f;  
            for (int i = 0; i < 5; i++)  
            {  
                float normalized = scores[i] / sum;  
                if (normalized > bestScore)  
                {  
                    bestScore = normalized;  
                    best = i;  
                }  
            }  
  
            confidence = bestScore;  
            return best;  
        }  
    }  
  
    public enum EPaddleType  
    {  
        Zero = 0,  
        Repeat = 1,  
        Loop = 2,  
    }  
}

```



`Packages/com.hero.lipsync/Runtime/LipSync_Job.cs` — 说明：新增帧内归一化 Job 与 Formant 分类 Job，同时保留并行化的卷积 / clarity / 能量计算 Job。  
  
```csharp  
```csharp  
using System;  
using Unity.Burst;  
using Unity.Collections;  
using Unity.Jobs;  
using Unity.Mathematics;  
using UnityEngine;  
  
namespace hero.LipSync.Runtime  
{  
    /// <summary>  
    ///  数据预处理 / 分类 Jobs  
    /// </summary>  
    [BurstCompile]  
    public struct GetSmoothSpectrum : IJobParallelFor  
    {  
        [ReadOnly] public int filterLength;  
        [ReadOnly] public EPaddleType paddleType;  
        [ReadOnly] public VowelInfomation vowelInfomation;  
        [NativeDisableParallelForRestriction]  
        [ReadOnly] public NativeArray<float> Spectrum;  
  
        [NativeDisableParallelForRestriction]  
        public NativeArray<float> SmoothedSpectrum;  
  
  
        public void Execute(int index)  
        {  
            LipSync_Algo.Convolute(Spectrum, vowelInfomation.GaussianFilter, paddleType, SmoothedSpectrum, filterLength, index);  
        }  
    }  
  
    // 帧内归一化（in-place）  
    [BurstCompile]  
    public struct NormalizeSpectrum : IJob  
    {  
        public NativeArray<float> SmoothedSpectrum;  
  
        public void Execute()  
        {  
            float maxVal = 0f;  
            for (int i = 0; i < SmoothedSpectrum.Length; i++)  
            {  
                float v = SmoothedSpectrum[i];  
                if (v > maxVal) maxVal = v;  
            }  
  
            if (maxVal <= 1e-6f) return;  
  
            float inv = 1f / maxVal;  
            for (int i = 0; i < SmoothedSpectrum.Length; i++)  
            {  
                SmoothedSpectrum[i] *= inv;  
            }  
        }  
    }  
  
    [BurstCompile]  
    public struct GetClarity : IJob  
    {  
        [ReadOnly] public int sampleRate;  
        [ReadOnly] public NativeArray<float> smoothedSpectrum;  
  
        public NativeArray<float> speechClarity;  
  
  
        public void Execute()  
        {  
  
            speechClarity[0] = LipSync_Algo.CalculateFrequencyBandRatio(smoothedSpectrum, 300f, 3400f, sampleRate); // 语音清晰度评分  
        }  
    }  
  
    /// <summary>  
    /// 并行处理每个元音（能量法）  
    /// </summary>  
    [BurstCompile]  
    public struct LipSyncJob : IJobParallelFor  
    {  
        [ReadOnly] public NativeArray<float> speechClarity;  
        [ReadOnly] public int sampleRate;  
        [ReadOnly] public VowelInfomation vowelInfomation;  
        [ReadOnly] public NativeArray<float> SmoothedSpectrum;  
  
        public NativeArray<float> peakValue;  
  
  
        public void Execute(int index)  
        {  
            peakValue[index] = LipSync_Algo.GetFrequencyBandEnergy(SmoothedSpectrum, vowelInfomation.POfBegin[index], vowelInfomation.POfEnd[index], sampleRate) * speechClarity[0];  
            peakValue[index] = math.pow(peakValue[index], vowelInfomation.PowOfAEIOU);  
        }  
    }  
  
    // 基于共振峰的轻量分类（单帧）  
    [BurstCompile]  
    public struct FormantClassifyJob : IJob  
    {  
        [ReadOnly] public NativeArray<float> SmoothedSpectrum;  
        [ReadOnly] public int sampleRate;  
  
        // 输出：检测到的元音索引（-1 表示无），以及置信度  
        public NativeArray<int> DetectedVowel;  
        public NativeArray<float> DetectedConfidence;  
  
        public void Execute()  
        {  
            float f1, f2;  
            LipSync_Algo.EstimateFormants(SmoothedSpectrum, sampleRate, out f1, out f2);  
            float conf;  
            int idx = LipSync_Algo.ClassifyVowelByFormants(f1, f2, out conf);  
            DetectedVowel[0] = idx;  
            DetectedConfidence[0] = conf;  
        }  
    }  
}

```

`Packages/com.hero.lipsync/Runtime/LipSync_JobEnv.cs` — 说明：整合调度逻辑，增加 EMA 自适应阈值、帧间平滑（previousPeakValues、smoothed confidence）、并发运行能量法与 Formant 分类，最终根据置信度选择输出或回退到能量法；注意 NativeArray 的分配与释放。  
  
```csharp  
```csharp  
using System.Linq;  
using Unity.Collections;  
using Unity.Jobs;  
using UnityEngine;  
  
namespace hero.LipSync.Runtime  
{  
    public class LipSync_JobEnv  
    {  
        // 声音相关内容  
        private VowelInfomation vowelInfomation;  
        private float[] _pOfBegin = { 600f, 400f, 200f, 400f, 300f };  
        private float[] _pOfEnd = { 1400f, 2500f, 3000f, 1000f, 900f };  
        private string[] CurrentVowelsString = { "A", "E", "I", "O", "U" };  
  
        // 高斯滤波器参数  
        public static readonly int FILTER_SIZE = 7;  
        public static readonly float FILTER_DEVIATION_SQUARE = 5.0f;  
  
  
        // 阈值 -- 声音过小则抛弃 ，  
        private float _amplitudeThreshold = 0.01f;  
        private int _sampleRate;  
  
        // EMA 用于自适应阈值  
        private float _amplitudeEMA = 0f;  
        private const float AMP_EMA_ALPHA = 0.2f;  
  
        // 帧间时间平滑（保存上帧结果）  
        private float[] _previousPeakValues;  
  
        #region Job  
  
        private JobHandle _lipSyncHandle;  
  
        private VowelInfomation _vowelInfomation;  
  
        private NativeArray<float> _spectrum;  
        private NativeArray<float> _smoothedSpectrum;  
        private bool _tooLow;  
        private NativeArray<float> _speechClarity;  
        private NativeArray<float> _peakValue;  
  
        // 新增：formant 检测输出  
        private NativeArray<int> _detectedVowel;  
        private NativeArray<float> _detectedConfidence;  
  
        #endregion  
  
        // 平滑保留  
        private int _previousVowelIndex = -1;  
        private float _smoothedConfidence = 0f;  
  
        public LipSync_JobEnv(int sampleRate)  
        {  
            _sampleRate = sampleRate;  
  
            vowelInfomation.GaussianFilter = LipSync_Algo.GenerateGaussianFilter(FILTER_SIZE, FILTER_DEVIATION_SQUARE);  
            vowelInfomation.POfBegin = new NativeArray<float>(_pOfBegin, Allocator.Persistent);  
            vowelInfomation.POfEnd = new NativeArray<float>(_pOfEnd, Allocator.Persistent);  
            vowelInfomation.VowelSize = 5;  
            vowelInfomation.PowOfAEIOU = 1.2f;  
  
            _previousPeakValues = new float[CurrentVowelsString.Length];  
        }  
  
  
        public void OnUpdate(float[] spectrum, ref LipSync_Info info)  
        {  
            Allocate(spectrum);  
            ScheduleJob();  
            GetVowelInfo(ref info);  
            DisPose();  
        }  
  
        public void DisposeVowelInfomation()  
        {  
            vowelInfomation.Dispose();  
        }  
  
        #region Func: 内存分配  
  
        // 分配 Job 内存  
        private void Allocate(float[] spectrum)  
        {  
            // 资源准备  
            _spectrum = new NativeArray<float>(spectrum, Allocator.TempJob);  
            _smoothedSpectrum = new NativeArray<float>(spectrum.Length, Allocator.TempJob);  
            _tooLow = false;  
            _speechClarity = new NativeArray<float>(1, Allocator.TempJob);  
            _peakValue = new NativeArray<float>(CurrentVowelsString.Length, Allocator.TempJob);  
  
            _detectedVowel = new NativeArray<int>(1, Allocator.TempJob);  
            _detectedConfidence = new NativeArray<float>(1, Allocator.TempJob);  
            _detectedVowel[0] = -1;  
            _detectedConfidence[0] = 0f;  
        }  
  
  
        // 释放内存  
        private void DisPose()  
        {  
            _spectrum.Dispose();  
            _smoothedSpectrum.Dispose();  
            _tooLow = false;  
            _peakValue.Dispose();  
            _speechClarity.Dispose();  
  
            _detectedVowel.Dispose();  
            _detectedConfidence.Dispose();  
        }  
  
        #endregion  
  
        private void GetVowelInfo(ref LipSync_Info info)  
        {  
  
            // 等待所有调度的 job 完成  
            _lipSyncHandle.Complete();  
  
  
            int pos = -1;  
            if (_tooLow == false)  
            {  
                // 优先使用 formant 分类结果（带置信度和平滑）  
                int raw = _detectedVowel[0];  
                float rawConf = _detectedConfidence[0];  
  
                // 指数平滑置信度，减少瞬变  
                _smoothedConfidence = Mathf.Lerp(_smoothedConfidence, rawConf, 0.5f);  
  
                if (raw >= 0 && _smoothedConfidence > 0.22f) // 可调阈值  
                {  
                    pos = raw;  
                }  
                else  
                {  
                    // 回退到能量分布法（保留原有并加入帧间平滑）  
                    int n = CurrentVowelsString.Length;  
                    float[] peaks = new float[n];  
                    float totalMouthWeight = 0f;  
                    for (int i = 0; i < n; i++)  
                    {  
                        peaks[i] = _peakValue[i];  
                        // 与上一帧结合，减少抖动  
                        peaks[i] = Mathf.Lerp(_previousPeakValues[i], peaks[i], 0.6f);  
                        _previousPeakValues[i] = peaks[i];  
                        totalMouthWeight += peaks[i];  
                    }  
  
                    if (totalMouthWeight > 0f)  
                    {  
                        for (int i = 0; i < n; i++)  
                        {  
                            peaks[i] /= totalMouthWeight;  
                        }  
  
                        float max = 0f;  
                        for (int i = 0; i < n; i++)  
                        {  
                            if (peaks[i] > max)  
                            {  
                                pos = i;  
                                max = peaks[i];  
                            }  
                        }  
                    }  
                }  
            }  
  
            info.Index = pos;  
            info.Vowel = pos == -1 ? "" : CurrentVowelsString[pos];  
        }  
  
        /// <summary>  
        ///  使用 JobSystem 并行的处理几个元音，同时运行 formant 分类  
        /// </summary>  
        private void ScheduleJob()  
        {  
  
            float sum = LipSync_Algo.GetSpectrumSum(_spectrum);  
  
            // 更新 EMA 并使用自适应阈值  
            _amplitudeEMA = AMP_EMA_ALPHA * sum + (1f - AMP_EMA_ALPHA) * _amplitudeEMA;  
            float adaptiveThreshold = Mathf.Max(_amplitudeThreshold, _amplitudeEMA * 0.35f);  
  
            _tooLow = sum < adaptiveThreshold;  
  
            if (_tooLow) return;  
  
            int filterMiddlePoint = Mathf.FloorToInt(vowelInfomation.GaussianFilter.Length / 2.0f);  
            GetSmoothSpectrum getSmoothSpectrum = new GetSmoothSpectrum()  
            {  
                filterLength = filterMiddlePoint,  
                paddleType = EPaddleType.Repeat,  
                vowelInfomation = vowelInfomation,  
                Spectrum = _spectrum,  
  
                SmoothedSpectrum = _smoothedSpectrum,  
            };  
  
            GetClarity getClarity = new GetClarity()  
            {  
                sampleRate =  _sampleRate,  
                smoothedSpectrum = _smoothedSpectrum,  
  
                speechClarity = _speechClarity  
            };  
  
            // 先做卷积  
            JobHandle getSmoothHandle = getSmoothSpectrum.Schedule(_spectrum.Length, 64);  
  
            // 帧内归一化（in-place）  
            NormalizeSpectrum normalize = new NormalizeSpectrum()  
            {  
                SmoothedSpectrum = _smoothedSpectrum  
            };  
            JobHandle normalizeHandle = normalize.Schedule(getSmoothHandle);  
  
            // clarity 在归一化后执行  
            JobHandle getClarityHandle = getClarity.Schedule(normalizeHandle);  
  
            // 并行计算能量法（每个元音）  
            LipSyncJob lipSyncJob = new LipSyncJob()  
            {  
                speechClarity = _speechClarity,  
                sampleRate = _sampleRate,  
                SmoothedSpectrum = _smoothedSpectrum,  
                vowelInfomation = vowelInfomation,  
  
                peakValue = _peakValue,  
            };  
            JobHandle lipSyncHandle = lipSyncJob.Schedule(CurrentVowelsString.Length, 2, getClarityHandle);  
  
            // 同时运行 Formant 分类 Job（单帧）  
            FormantClassifyJob classify = new FormantClassifyJob()  
            {  
                SmoothedSpectrum = _smoothedSpectrum,  
                sampleRate = _sampleRate,  
                DetectedVowel = _detectedVowel,  
                DetectedConfidence = _detectedConfidence  
            };  
            JobHandle classifyHandle = classify.Schedule(getClarityHandle);  
  
            // 合并依赖，后续主线程等待合并的 handle  
            _lipSyncHandle = JobHandle.CombineDependencies(lipSyncHandle, classifyHandle);  
        }  
    }  
}
```


说明结束。以上改动已涵盖：帧内归一化、帧间与置信度平滑、自适应阈值、共振峰估计与基于 F1/F2 的分类、以及能量法回退路径。将这些文件替换/更新到项目中后建议：  
- 在不同说话者/音量/噪声下实测并调整 `means`、sigma 值、置信度阈值和 EMA 系数以获得最佳效果。