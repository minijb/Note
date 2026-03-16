
## 1. ChannelGroup 

可以附着在其他物件上， 添加声音或者进行监视

## 2. DSP  数字信号处理器

用于获取声音数据的工具

## 3. DSP_PARAMETER_FFT 

快速傅里叶变换选项

https://fmod.com/docs/2.03/api/plugin-api-dsp.html#fmod_dsp_parameter_fft


## 4.创建和销毁一个DSP


```c#
private DSP _dsp; // 数据处理器
private DSP_PARAMETER_FFT _fftParam = default;
private ChannelGroup _channelGroup = default; // 通道组 -- 用于监控


/// <summary>
///  创建 DSP 并附加到 EventInstance 上
/// </summary>
/// <param name="eventInstance">对应的 event</param>
/// <returns>一个 DSP 实例</returns>
private DSP CreateDSP(EventInstance eventInstance)
{
	DSP dsp;
	FMOD.RESULT result;

	result = FMODUnity.RuntimeManager.CoreSystem.createDSPByType(FMOD.DSP_TYPE.FFT, out dsp);
	if (result != FMOD.RESULT.OK)
		ReportError("Create DSP failed: ");

	result = dsp.setParameterInt((int)FMOD.DSP_FFT.WINDOW, (int)WINDOW_TYPE);
	if (result != FMOD.RESULT.OK)
		ReportError("Set DSP parameter failed: ");
	result = dsp.setParameterInt((int)FMOD.DSP_FFT.WINDOWSIZE, WINDOW_SIZE * 2);
	if (result != FMOD.RESULT.OK)
		ReportError("Set DSP parameter failed: ");


	FMODUnity.RuntimeManager.StudioSystem.flushCommands();

	// attach dsp to the channelGroup of event instance
	result = eventInstance.getChannelGroup(out ChannelGroup channelGroup);
	if (result != FMOD.RESULT.OK)
		ReportError("Get ChannelGroup from EventInstance failed: ");
	_channelGroup = channelGroup;
	result = channelGroup.addDSP(FMOD.CHANNELCONTROL_DSP_INDEX.HEAD, dsp);
	if (result != FMOD.RESULT.OK)
		ReportError("Add DSP to ChannelGroup failed: ");

	return dsp;
}


private void ClearDSP()
{
	FMOD.RESULT result;
	_channelGroup.removeDSP(_dsp);
	result = _dsp.release();
	if (result != FMOD.RESULT.OK)
		ReportError("Release DSP failed: ");
	_dsp = default;
	_channelGroup = default;
}

```


**注意点**

- DSP 在 `setParameterXXX` 需要 `	FMODUnity.RuntimeManager.StudioSystem.flushCommands();`
- 清理的时候，需要先在 channelGroup 上移除 dsp 然后释放。

## 5. 获取频谱信息

```c#
private void GetSpectrumData()
{
	if (!_dsp.hasHandle()) return;
	System.IntPtr _data;
	uint _length;

	if (_dsp.getParameterData((int)FMOD.DSP_FFT.SPECTRUMDATA, out _data, out _length) != FMOD.RESULT.OK) return;
	_fftParam = (FMOD.DSP_PARAMETER_FFT)Marshal.PtrToStructure(_data, typeof(DSP_PARAMETER_FFT));

	if (_fftParam.numchannels > 0)
	{
		_fftParam.getSpectrum(0, ref _spectrum);
	}
	
}

```