
```c#
	public class RichTextProcessor
	{
		public RichTextTagInfo[] supportedTags;
		public bool emojisAllowed;
		public bool richTextBindingsAllowed;

		public TextEditFrame LastRichTextEditFrame { get; private set; }
		public TextEditFrame LastTextEditFrame { get; private set; }

		private List<TextRegion> textRegions;
		private StringBuilder stringBuilder;
		public string RichText { get { return LastRichTextEditFrame.text; } }
		public string Text { get { return LastTextEditFrame.text; } }
		public List<TextRegion> TextRegions { get { return textRegions; } }

		public RichTextProcessor(RichTextTagInfo[] supportedTags, bool emojisAllowed, bool richTextBindingsAllowed)
		{
			this.supportedTags = supportedTags;
			this.emojisAllowed = emojisAllowed;
			this.richTextBindingsAllowed = richTextBindingsAllowed;
			this.textRegions = new List<TextRegion>();
			this.stringBuilder = new StringBuilder();
		}

		public void SetupRichText(string richText)
		{
			textRegions.Clear();
			List<RichTextRegion> richTextRegions = ParseRichTextRegions(richText);
			List<TextRegion> parsedTextRegions = new List<TextRegion>();

			int length = richTextRegions.Count;
			for(int i = 0; i < length; i++)
			{
				RichTextRegion richTextRegion = richTextRegions[i];
				List<TextRegion> currentTextRegions = ParseTextRegions(richTextRegion.Text);
				foreach(TextRegion currentTextRegion in currentTextRegions)
				{
					currentTextRegion.ConfigureRichTextRegion(richTextRegion);
					parsedTextRegions.Add(currentTextRegion);
				}
			}

			length = parsedTextRegions.Count;
			if(length == 1)
			{
				textRegions.Add(parsedTextRegions[0]);
			}
			else
			{
				for(int i = 0; i < length; i++)
				{
					TextRegion region = parsedTextRegions[i];
					if(region.isSymbol) //Symbols can't be merged
					{
						region.ConfigureSymbol();
						textRegions.Add(region);
						continue;
					}

					int mergedIndex = i;
					for(int ni = i + 1; ni < length; ni++)
					{
						TextRegion nextRegion = parsedTextRegions[ni];
						if(nextRegion.isSymbol) //Symbols can't be merged
						{
							break;
						}
						else
						{
							region.Content = region.content + nextRegion.content;
							region.richTextRegions.Add(nextRegion.richTextRegions[0]);
							mergedIndex = ni;
						}
					}

					textRegions.Add(region);
					i = mergedIndex;
				}
			}

			string resultRichText = RebuildRichTextString();
			string resultText = RebuildTextString();
			LastRichTextEditFrame = new TextEditFrame(resultRichText, 0, 0);
			LastTextEditFrame = new TextEditFrame(resultText, 0, 0);
		}

		public string RebuildRichTextString()
		{
			stringBuilder.Clear();

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				textRegions[i].BuildRichTextString(stringBuilder);
			}

			return stringBuilder.ToString();
		}

		public string RebuildTextString()
		{
			stringBuilder.Clear();

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				stringBuilder.Append(textRegions[i].content);
			}

			return stringBuilder.ToString();
		}

		public List<RichTextRegion> ParseRichTextRegions(string richText)
		{
			if(emojisAllowed || richTextBindingsAllowed)
			{
				richText = ConvertSpecialTags(richText);
			}
			List<RichTextRegion> regions = new List<RichTextRegion>();
			if(string.IsNullOrEmpty(richText)) { return regions; }

			Stack<string> startTagsStack = new Stack<string>();
			Stack<string> endTagsStack = new Stack<string>();
			int tagStartIndex = -1;
			int tagEndIndex = -1;

			int length = richText.Length;
			for(int i = 0; i < length; i++)
			{
				char c = richText[i];
				if(c == '<')
				{
					if(tagStartIndex != -1) //Wasn't a tag
					{
						if(tagEndIndex == -1)
						{
							int amount = i - tagStartIndex;
							string content = richText.Substring(0, amount);
							regions.Add(new RichTextRegion(content));
							tagEndIndex += amount;
						}
						else
						{
							int amount = tagStartIndex - tagEndIndex;
							string content = richText.Substring(tagEndIndex + 1, amount);
							regions.Add(new RichTextRegion(content, new List<string>(startTagsStack), new List<string>(endTagsStack)));
							tagEndIndex += amount;
						}
					}
					tagStartIndex = i;
				}
				else if(c == '>' && tagStartIndex != -1)
				{
					string tagText = richText.Substring(tagStartIndex, (i - tagStartIndex) + 1);

					bool isStartTag = IsValidStartTagText(tagText, out int si);
					if(isStartTag)
					{
						if(tagEndIndex == -1 && tagStartIndex != 0)
						{
							string content = richText.Substring(0, tagStartIndex);
							regions.Add(new RichTextRegion(content));
						}
						else if(tagEndIndex + 1 != tagStartIndex)
						{
							int amount = tagStartIndex - (tagEndIndex + 1);
							string content = richText.Substring(tagEndIndex + 1, amount);
							regions.Add(new RichTextRegion(content, new List<string>(startTagsStack), new List<string>(endTagsStack)));
						}

						startTagsStack.Push(tagText); //Use tag text here to preserve the parameter value
						endTagsStack.Push(supportedTags[si].endTag);

						tagStartIndex = -1;
						tagEndIndex = i;
						continue;
					}

					bool isEndTag = IsValidEndTagText(tagText, out int ei);
					if(isEndTag)
					{
						if(tagEndIndex + 1 != tagStartIndex)
						{
							int amount = tagStartIndex - (tagEndIndex + 1);
							string content = richText.Substring(tagEndIndex + 1, amount);
							regions.Add(new RichTextRegion(content, new List<string>(startTagsStack), new List<string>(endTagsStack)));
						}

						startTagsStack.Pop();
						endTagsStack.Pop();

						tagStartIndex = -1;
						tagEndIndex = i;
						continue;
					}
				}
			}

			if(tagEndIndex != -1)
			{
				if(tagEndIndex < length - 1)
				{
					int amount = length - (tagEndIndex + 1);
					string content = richText.Substring(tagEndIndex + 1, amount);
					regions.Add(new RichTextRegion(content, null, null));
				}
			}
			else
			{
				regions.Add(new RichTextRegion(richText, null, null));
			}

			return regions;
		}

		private string ConvertSpecialTags(string richText)
		{
			StringBuilder stringBuilder = new StringBuilder();
			int tagStartIndex = -1;

			int length = richText.Length;
			for(int i = 0; i < length; i++)
			{
				char c = richText[i];
				if(c == '<')
				{
					if(tagStartIndex != -1)
					{
						string text = richText.Substring(tagStartIndex, i - tagStartIndex);
						stringBuilder.Append(text);
					}
					tagStartIndex = i;
				}
				else if(c == '>' && tagStartIndex != -1)
				{
					string tagText = richText.Substring(tagStartIndex, (i - tagStartIndex) + 1);

					if(emojisAllowed && IsValidSingleTagText(tagText) && NativeKeyboardManager.EmojiEngine.TryGetSprite(tagText, out EmojiData emojiData))
					{
						stringBuilder.Append(emojiData.text);
					}
					else if(richTextBindingsAllowed && NativeKeyboardManager.RichTextBindingEngine.TryFindNextBindingInRichText(richText, tagStartIndex, out RichTextBindingData tagData))
					{
						stringBuilder.Append(tagData.codePoint);
						i = tagStartIndex + tagData.richText.Length - 1;
					}
					else
					{
						stringBuilder.Append(tagText);
					}

					tagStartIndex = -1;
				}
				else if(tagStartIndex == -1)
				{
					stringBuilder.Append(c);
				}
			}

			if(tagStartIndex != -1)
			{
				stringBuilder.Append(richText.Substring(tagStartIndex));
			}

			return stringBuilder.ToString();
		}

		public bool IsValidSingleTagText(string tagText)
		{
			int length = supportedTags.Length;
			for(int i = 0; i < length; i++)
			{
				RichTextTagInfo tagInfo = supportedTags[i];
				switch(tagInfo.type)
				{
					case RichTextTagType.BASIC_SINGLE_TAG:
						if(tagInfo.startTag == tagText)
						{
							return true;
						}
						break;
					case RichTextTagType.SINGLE_PARAMETER_SINGLE_TAG:
						if(tagText.StartsWith(tagInfo.startTagStart))
						{
							return true;
						}
						break;

				}
			}

			return false;
		}

		public List<TextRegion> ParseTextRegions(string text)
		{
			List<TextRegion> regions = new List<TextRegion>();
			StringBuilder stringBuilder = new StringBuilder();

			int length = text.Length;
			for(int i = 0; i < length; i++)
			{
				char c = text[i];
				if(richTextBindingsAllowed && NativeKeyboardManager.RichTextBindingEngine.TryGetBindingFromCodePoint(c, out RichTextBindingData tagData))
				{
					if(stringBuilder.Length > 0)
					{
						string content = stringBuilder.ToString();
						regions.Add(new TextRegion(content));
						stringBuilder.Clear();
					}

					regions.Add(new TextRegion(tagData));
				}
				else if(emojisAllowed && NativeKeyboardManager.EmojiEngine.TryFindNextEmojiInText(text, i, out EmojiData emojiData))
				{
					if(stringBuilder.Length > 0)
					{
						string content = stringBuilder.ToString();
						regions.Add(new TextRegion(content));
						stringBuilder.Clear();
					}

					regions.Add(new TextRegion(emojiData));
					i += (emojiData.text.Length - 1);
				}
				else
				{
					stringBuilder.Append(c);
				}
			}

			if(stringBuilder.Length > 0)
			{
				string content = stringBuilder.ToString();
				regions.Add(new TextRegion(content));
			}

			return regions;
		}

		public bool IsValidTagText(string tagText)
		{
			int length = supportedTags.Length;
			for(int i = 0; i < length; i++)
			{
				RichTextTagInfo tagInfo = supportedTags[i];
				switch(tagInfo.type)
				{
					case RichTextTagType.BASIC_TAG_PAIR:
						if(tagInfo.startTag == tagText || tagInfo.endTag == tagText)
						{
							return true;
						}
						break;
					case RichTextTagType.SINGLE_PARAMETER_TAG_PAIR:
						if(tagText.StartsWith(tagInfo.startTagStart) || tagInfo.endTag == tagText)
						{
							return true;
						}
						break;
					case RichTextTagType.SINGLE_PARAMETER_SINGLE_TAG:
						if(tagText.StartsWith(tagInfo.startTagStart))
						{
							return true;
						}
						break;

				}
			}

			return false;
		}

		public bool IsValidStartTagText(string tagText, out int index)
		{
			int length = supportedTags.Length;
			for(int i = 0; i < length; i++)
			{
				RichTextTagInfo tagInfo = supportedTags[i];
				switch(tagInfo.type)
				{
					case RichTextTagType.BASIC_TAG_PAIR:
						if(tagInfo.startTag == tagText)
						{
							index = i;
							return true;
						}
						break;
					case RichTextTagType.SINGLE_PARAMETER_TAG_PAIR:
						if(tagText.StartsWith(tagInfo.startTagStart))
						{
							index = i;
							return true;
						}
						break;

				}
			}

			index = -1;
			return false;
		}

		public bool IsValidEndTagText(string tagText, out int index)
		{
			int length = supportedTags.Length;
			for(int i = 0; i < length; i++)
			{
				RichTextTagInfo tagInfo = supportedTags[i];
				if(tagInfo.endTag == tagText)
				{
					index = i;
					return true;
				}
			}

			index = -1;
			return false;
		}

		/// <summary>Processes a TextEditFrame in rich text to a TextEditFrame in original text</summary>
		public TextEditFrame ProcessRichTextEditFrame(TextEditFrame richTextEditFrame)
		{
			TextEditFrame textEditFrame = new TextEditFrame();
			if(LastRichTextEditFrame.text == richTextEditFrame.text) //No text change
			{
				textEditFrame.text = LastTextEditFrame.text;

				if(richTextEditFrame.selectionStartPosition == LastRichTextEditFrame.selectionStartPosition) //No change
				{
					textEditFrame.selectionStartPosition = LastTextEditFrame.selectionStartPosition;
				}
				else //Selection start position changed
				{
					textEditFrame.selectionStartPosition = DeterminePositionInText(richTextEditFrame.selectionStartPosition, textEditFrame.text);
				}

				if(richTextEditFrame.selectionEndPosition == LastRichTextEditFrame.selectionEndPosition) //No change
				{
					textEditFrame.selectionEndPosition = LastTextEditFrame.selectionEndPosition;
				}
				else //Selection end position changed
				{
					if(richTextEditFrame.selectionStartPosition == richTextEditFrame.selectionEndPosition) //No selection
					{
						textEditFrame.selectionEndPosition = textEditFrame.selectionStartPosition;
					}
					else
					{
						textEditFrame.selectionEndPosition = DeterminePositionInText(richTextEditFrame.selectionEndPosition, textEditFrame.text);
					}
				}
			}
			else
			{
				Debug.LogWarning("Shouldn't be executed here. Rich Text changes should call SetupRichText()");
			}

			LastTextEditFrame = textEditFrame;
			LastRichTextEditFrame = richTextEditFrame;
			return textEditFrame;
		}

		/// <summary>Processes a TextEditFrame in original text to a TextEditFrame in rich text</summary>
		public TextEditFrame ProcessTextEditFrame(TextEditFrame textEditFrame)
		{
			TextEditFrame richTextEditFrame = new TextEditFrame();
			if(textEditFrame.text == LastTextEditFrame.text) //No text change
			{
				richTextEditFrame.text = LastRichTextEditFrame.text;

				if(textEditFrame.selectionStartPosition == LastTextEditFrame.selectionStartPosition) //No selection start position change
				{
					richTextEditFrame.selectionStartPosition = LastRichTextEditFrame.selectionStartPosition;
				}
				else //Selection start position changed
				{
					richTextEditFrame.selectionStartPosition = DeterminePositionInRichText(textEditFrame.selectionStartPosition, richTextEditFrame.text);
				}

				if(textEditFrame.selectionEndPosition == LastTextEditFrame.selectionEndPosition) //No selection end position change
				{
					richTextEditFrame.selectionEndPosition = LastRichTextEditFrame.selectionEndPosition;
				}
				else //Selection end position changed
				{
					if(textEditFrame.selectionStartPosition == textEditFrame.selectionEndPosition) //No selection
					{
						richTextEditFrame.selectionEndPosition = richTextEditFrame.selectionStartPosition;
					}
					else //Has selection
					{
						richTextEditFrame.selectionEndPosition = DeterminePositionInRichText(textEditFrame.selectionEndPosition, richTextEditFrame.text);
					}
				}
			}
			else //Text change
			{
				if(textEditFrame.selectionStartPosition == textEditFrame.selectionEndPosition && LastTextEditFrame.selectionStartPosition != LastTextEditFrame.selectionEndPosition) //Selection cleared
				{
					int previousSelectionAmount = LastTextEditFrame.selectionEndPosition - LastTextEditFrame.selectionStartPosition;
					int insertAmount = textEditFrame.text.Length - (LastTextEditFrame.text.Length - previousSelectionAmount);
					if(insertAmount > 0) //Clear & insert
					{
						DeleteInText(textEditFrame.selectionStartPosition - insertAmount, previousSelectionAmount); //Forward delete from current position
                        int start = textEditFrame.selectionStartPosition - insertAmount;
                        if (start < 0) start = 0;
                        string textToInsert = textEditFrame.text.Substring(start, insertAmount);
						InsertInText(textToInsert, textEditFrame.selectionStartPosition - insertAmount);
					}
					else //Only clear
					{
						DeleteInText(textEditFrame.selectionStartPosition, previousSelectionAmount); //Forward delete from current position
					}
				}
				else //No selection change
				{
					int amount = Mathf.Abs(textEditFrame.text.Length - LastTextEditFrame.text.Length);
					if(textEditFrame.selectionStartPosition > LastTextEditFrame.selectionStartPosition) //Text insert
					{
						if(CheckWordReplaced(textEditFrame.text, LastTextEditFrame.text, LastTextEditFrame.selectionStartPosition, out int wordStartPosition))
						{
							int deleteAmount = (LastTextEditFrame.selectionStartPosition - wordStartPosition);
							DeleteInText(LastTextEditFrame.selectionStartPosition - deleteAmount, deleteAmount);
							amount += deleteAmount;
                            int start = LastTextEditFrame.selectionStartPosition - deleteAmount;
                            if (start < 0) start = 0;
                            string textToInsert = textEditFrame.text.Substring(start, amount);
							InsertInText(textToInsert, LastTextEditFrame.selectionStartPosition - deleteAmount);
						}
						else
                        {
                            int start = LastTextEditFrame.selectionStartPosition;
                            if (start < 0) start = 0;
                            string textToInsert = textEditFrame.text.Substring(start, amount);
							InsertInText(textToInsert, LastTextEditFrame.selectionStartPosition);
						}
					}
					else if(textEditFrame.selectionStartPosition < LastTextEditFrame.selectionStartPosition) //Backwards delete
					{
						DeleteInText(textEditFrame.selectionStartPosition, amount); //Forward delete from current position
						if(CheckWordReplaced(textEditFrame.text, LastTextEditFrame.text, textEditFrame.selectionStartPosition, out int wordStartPosition))
						{
							int deleteAmount = (textEditFrame.selectionStartPosition - wordStartPosition);
							DeleteInText(textEditFrame.selectionStartPosition - deleteAmount, deleteAmount);
							amount = deleteAmount;
                            int start = textEditFrame.selectionStartPosition - deleteAmount;
                            if (start < 0) start = 0;
                            string textToInsert = textEditFrame.text.Substring(start, amount);
							InsertInText(textToInsert, textEditFrame.selectionStartPosition - deleteAmount);
						}
					}
					else if(amount > 0) //Forward delete
					{
						DeleteInText(textEditFrame.selectionStartPosition, amount); //Forward delete from current position
					}
					else if(CheckWordReplaced(textEditFrame.text, LastTextEditFrame.text, textEditFrame.selectionStartPosition, out int wordStartPosition))
					{
						int deleteAmount = (textEditFrame.selectionStartPosition - wordStartPosition);
						DeleteInText(textEditFrame.selectionStartPosition - deleteAmount, deleteAmount);
						amount = deleteAmount;
                        int start = textEditFrame.selectionStartPosition - deleteAmount;
                        if (start < 0) start = 0;
                        string textToInsert = textEditFrame.text.Substring(start, amount);
						InsertInText(textToInsert, textEditFrame.selectionStartPosition - deleteAmount);
					}
				}

				richTextEditFrame.text = RebuildRichTextString();
				richTextEditFrame.selectionStartPosition = DeterminePositionInRichText(textEditFrame.selectionStartPosition, richTextEditFrame.text);
				richTextEditFrame.selectionEndPosition = richTextEditFrame.selectionStartPosition;
			}

			LastTextEditFrame = textEditFrame;
			LastRichTextEditFrame = richTextEditFrame;

			return richTextEditFrame;
		}

		public bool CheckWordReplaced(string currentText, string lastText, int textPosition, out int wordStartPosition)
		{
			int currentLength = currentText.Length;
			int lastLength = lastText.Length;
			wordStartPosition = -1;
			bool detectedWordChange = false;

			for(int i = textPosition - 1; i >= 0; i--)
			{
				if(i < currentLength && i < lastLength)
				{
					char currentChar = currentText[i];
					if(currentChar == ' ' || currentChar == '\n')
					{
						break;
					}

					char lastChar = lastText[i];
					if(currentChar == ' ' || currentChar == '\n')
					{
						break;
					}

					if(currentChar != lastChar)
					{
						wordStartPosition = i;
						detectedWordChange = true;
					}
				}
				else
				{
					break;
				}
			}

			return detectedWordChange;
		}

		public void InsertInText(string textToInsert, int textPosition)
		{
			List<TextRegion> insertRegions = ParseTextRegions(textToInsert);

			int length = insertRegions.Count;
			for(int i = 0; i < length; i++)
			{
				TextRegion insertRegion = insertRegions[i];
				string contentToInsert = insertRegion.content;
				bool hasInsertedRegion = false;
				int textOffset = 0;
				int previousTextOffset = 0;

				int regionsLength = textRegions.Count;
				if(regionsLength == 0) //Just insert
				{
					insertRegion.richTextRegions.Add(new RichTextRegion(contentToInsert));
					if(insertRegion.isSymbol)
					{
						insertRegion.ConfigureSymbol();
					}
					textRegions.Add(insertRegion);
					textPosition += contentToInsert.Length;
					continue;
				}
				else
				{
					for(int ri = 0; ri < regionsLength; ri++)
					{
						TextRegion textRegion = textRegions[ri];

						if(textRegion.PositionWithinRegion(textOffset, textPosition, out bool startOfRegion))
						{
							if(startOfRegion) //Add after previous text region
							{
								if(ri == 0)
								{
									insertRegion.richTextRegions.Add(new RichTextRegion(contentToInsert));
									if(insertRegion.isSymbol)
									{
										insertRegion.ConfigureSymbol();
									}

									textRegions.Insert(0, insertRegion);
									textPosition += contentToInsert.Length;
									hasInsertedRegion = true;
									break;
								}

								TextRegion previousRegion = textRegions[ri - 1];
								if(previousRegion.isSymbol) //Add after symbol
								{
									RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
									List<RichTextRegion> richTextRegions = previousRegion.richTextRegions;
									richTextRegion.CopyTags(richTextRegions[richTextRegions.Count - 1]);
									insertRegion.richTextRegions.Add(richTextRegion);

									if(insertRegion.isSymbol)
									{
										insertRegion.ConfigureSymbol();
									}

									textRegions.Insert(ri, insertRegion);
									textPosition += contentToInsert.Length;
								}
								else
								{
									if(insertRegion.isSymbol)
									{
										RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
										List<RichTextRegion> richTextRegions = previousRegion.richTextRegions;
										richTextRegion.CopyTags(richTextRegions[richTextRegions.Count - 1]);
										insertRegion.richTextRegions.Add(richTextRegion);

										insertRegion.ConfigureSymbol();

										textRegions.Insert(ri, insertRegion);
										textPosition += contentToInsert.Length;
									}
									else if(previousRegion.TryInsertInText(contentToInsert, previousTextOffset, textPosition))
									{
										textPosition += contentToInsert.Length;
									}
								}
							}
							else //Add in current text region
							{
								if(textRegion.isSymbol) //Add before symbol
								{
									RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
									if(ri > 0)
									{
										TextRegion previousRegion = textRegions[ri - 1];
										List<RichTextRegion> richTextRegions = previousRegion.richTextRegions;
										richTextRegion.CopyTags(richTextRegions[richTextRegions.Count - 1]);
									}
									insertRegion.richTextRegions.Add(richTextRegion);

									if(insertRegion.isSymbol)
									{
										insertRegion.ConfigureSymbol();
									}

									textRegions.Insert(ri, insertRegion);
									textPosition += contentToInsert.Length;
								}
								else
								{
									if(insertRegion.isSymbol)
									{
										TextRegion[] splitRegions = textRegion.SplitRegion(textOffset, textPosition);
										textRegions.RemoveAt(ri);
										textRegions.Insert(ri, splitRegions[0]);

										RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
										richTextRegion.CopyTags(splitRegions[0].richTextRegions[0]);
										insertRegion.richTextRegions.Add(richTextRegion);
										insertRegion.ConfigureSymbol();
										textRegions.Insert(ri + 1, insertRegion);
										textRegions.Insert(ri + 2, splitRegions[1]);

										textPosition += contentToInsert.Length;
									}
									else if(textRegion.TryInsertInText(contentToInsert, textOffset, textPosition))
									{
										textPosition += contentToInsert.Length;
									}
								}
							}
							hasInsertedRegion = true;
							break;
						}
						else
						{
							previousTextOffset = textOffset;
							textOffset += textRegion.content.Length;
						}
					}
				}

				if(!hasInsertedRegion)
				{
					if(regionsLength == 0)
					{
						insertRegion.richTextRegions.Add(new RichTextRegion(textToInsert));
						if(insertRegion.isSymbol)
						{
							insertRegion.ConfigureSymbol();
						}

						textRegions.Insert(0, insertRegion);
						textPosition += contentToInsert.Length;
						continue;
					}

					TextRegion previousRegion = textRegions[regionsLength - 1];
					if(previousRegion.isSymbol) //Add after symbol
					{
						RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
						List<RichTextRegion> richTextRegions = previousRegion.richTextRegions;
						richTextRegion.CopyTags(richTextRegions[richTextRegions.Count - 1]);
						insertRegion.richTextRegions.Add(richTextRegion);

						if(insertRegion.isSymbol)
						{
							insertRegion.ConfigureSymbol();
						}

						textRegions.Insert(regionsLength, insertRegion);
						textPosition += contentToInsert.Length;
					}
					else
					{
						if(insertRegion.isSymbol)
						{
							RichTextRegion richTextRegion = new RichTextRegion(contentToInsert);
							List<RichTextRegion> richTextRegions = previousRegion.richTextRegions;
							richTextRegion.CopyTags(richTextRegions[richTextRegions.Count - 1]);
							insertRegion.richTextRegions.Add(richTextRegion);

							insertRegion.ConfigureSymbol();

							textRegions.Insert(regionsLength, insertRegion);
							textPosition += contentToInsert.Length;
						}
						else if(previousRegion.TryInsertInText(contentToInsert, previousTextOffset, textPosition))
						{
							textPosition += contentToInsert.Length;
						}
					}
				}
			}

			//PrintTextRegions();
		}

		public void PrintTextRegions()
		{
			foreach(TextRegion textRegion in textRegions)
			{
				this.Log("TextRegion: " + textRegion);
				foreach(RichTextRegion richTextRegion in textRegion.richTextRegions)
				{
					this.Log("RichTextRegion: " + richTextRegion);
				}
			}
		}

		public void DeleteInText(int textPosition, int amount)
		{
			int textOffset = 0;
			int richTextOffset = 0;

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				TextRegion textRegion = textRegions[i];
				int startTextOffset = textOffset;
				int startRichTextOffset = richTextOffset;
				if(textRegion.TryDeleteInText(ref amount, ref richTextOffset, ref textOffset, textPosition))
				{
					if(textRegion.content.Length == 0)
					{
						textRegions.RemoveAt(i);
						length--;
					}

					if(amount == 0)
					{
						break;
					}
					else //Recheck to make sure that is there no more content to delete
					{
						textOffset = startTextOffset;
						richTextOffset = startRichTextOffset;
						i--;
					}
				}
			}
		}

		public TextEditFrame ToggleTagPair(string startTag, string endTag)
		{
			int start = LastTextEditFrame.selectionStartPosition;
			int end = LastTextEditFrame.selectionEndPosition;
			bool startFound = false;
			bool foundStart = false;
			bool toggleON = false;
			int textOffset = 0;

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				TextRegion textRegion = textRegions[i];
				if(startFound)
				{
					bool endFound = textRegion.ToggleTagPairInRichText(start, end, textOffset, startTag, endTag, ref foundStart, ref toggleON);
					if(endFound)
					{
						break;
					}
					else
					{
						textOffset += textRegion.content.Length;
					}
				}
				else
				{
					if(textRegion.PositionWithinRegion(textOffset, start, out bool startOfRegion))
					{
						startFound = true;
						i--; //Recheck
					}
					else
					{
						textOffset += textRegion.content.Length;
					}
				}
			}

			TextEditFrame textEditFrame = LastTextEditFrame;
			TextEditFrame richTextEditFrame = new TextEditFrame();
			richTextEditFrame.text = RebuildRichTextString();
			richTextEditFrame.selectionStartPosition = DeterminePositionInRichText(textEditFrame.selectionStartPosition, richTextEditFrame.text);
			richTextEditFrame.selectionEndPosition = DeterminePositionInRichText(textEditFrame.selectionEndPosition, richTextEditFrame.text); ;

			LastTextEditFrame = textEditFrame;
			LastRichTextEditFrame = richTextEditFrame;
			return richTextEditFrame;
		}

		public int DeterminePositionInText(int richTextPosition, string text)
		{
			int richTextOffset = 0;
			int textOffset = 0;

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				if(textRegions[i].TryDeterminePositionInText(richTextPosition, ref richTextOffset, ref textOffset, out int textPosition))
				{
					return textPosition;
				}
			}

			return text.Length;
		}

		public int DeterminePositionInRichText(int textPosition, string richText)
		{
			int richTextOffset = 0;
			int textOffset = 0;

			int length = textRegions.Count;
			for(int i = 0; i < length; i++)
			{
				if(textRegions[i].TryDeterminePositionInRichText(textPosition, ref richTextOffset, ref textOffset, out int richTextPosition))
				{
					return richTextPosition;
				}
			}

			return richText.Length;
		}
	}
```

`RichTextProcessor`

类用于处理富文本的解析和编辑。该类包含多个字段和方法，用于管理富文本标签、表情符号、文本绑定、文本区域等。类中定义了 `supportedTags`、`emojisAllowed` 和 `richTextBindingsAllowed` 字段，分别表示支持的富文本标签、是否允许表情符号以及是否允许富文本绑定。`LastRichTextEditFrame` 和 `LastTextEditFrame` 属性分别存储最后一次富文本编辑帧和文本编辑帧。`textRegions` 列表用于存储文本区域，`stringBuilder` 用于构建字符串。

构造函数 `RichTextProcessor` 初始化支持的标签、表情符号和富文本绑定，并创建 `textRegions` 列表和 `stringBuilder` 对象。`SetupRichText` 方法用于设置富文本，首先清空 `textRegions` 列表，然后解析富文本区域，并将其转换为文本区域。方法中遍历解析后的文本区域，并合并相邻的非符号区域。最后，重建富文本字符串和文本字符串，并更新最后一次富文本编辑帧和文本编辑帧。

`RebuildRichTextString` 方法用于重建富文本字符串，遍历 `textRegions` 列表，并调用每个文本区域的 `BuildRichTextString` 方法，将结果追加到 `stringBuilder` 中。`RebuildTextString` 方法用于重建文本字符串，遍历 `textRegions` 列表，并将每个文本区域的内容追加到 `stringBuilder` 中。

`ParseRichTextRegions` 方法用于解析富文本区域，首先检查是否允许表情符号或富文本绑定，如果允许，则转换特殊标签。方法中遍历富文本字符串，解析开始标签和结束标签，并将内容添加到 `regions` 列表中。`ConvertSpecialTags` 方法用于转换特殊标签，例如表情符号和富文本绑定。

`IsValidSingleTagText` 方法用于检查标签文本是否为有效的单标签，遍历支持的标签，并根据标签类型进行匹配。`ParseTextRegions` 方法用于解析文本区域，遍历文本字符串，解析表情符号和富文本绑定，并将内容添加到 `regions` 列表中。

`IsValidTagText` 方法用于检查标签文本是否为有效标签，遍历支持的标签，并根据标签类型进行匹配。`IsValidStartTagText` 方法用于检查标签文本是否为有效的开始标签，并返回标签索引。`IsValidEndTagText` 方法用于检查标签文本是否为有效的结束标签，并返回标签索引。

`ProcessRichTextEditFrame` 方法用于将富文本编辑帧转换为文本编辑帧，检查文本是否发生变化，并更新选择起始位置和结束位置。`ProcessTextEditFrame` 方法用于将文本编辑帧转换为富文本编辑帧，检查文本和选择是否发生变化，并更新富文本字符串和选择位置。

`CheckWordReplaced` 方法用于检查单词是否被替换，遍历文本字符，并比较当前字符和上一个字符。`InsertInText` 方法用于在文本中插入内容，解析插入的文本区域，并将其添加到 `textRegions` 列表中。`DeleteInText` 方法用于在文本中删除内容，遍历 `textRegions` 列表，并删除指定位置的内容。

`ToggleTagPair` 方法用于切换标签对，遍历 `textRegions` 列表，并在指定位置添加或删除标签对。`DeterminePositionInText` 方法用于确定富文本位置在文本中的位置，遍历 `textRegions` 列表，并计算文本位置。`DeterminePositionInRichText` 方法用于确定文本位置在富文本中的位置，遍历 `textRegions` 列表，并计算富文本位置。

通过这些方法和属性，`RichTextProcessor` 类提供了丰富的功能，用于解析和编辑富文本，包括标签解析、表情符号处理、文本绑定、文本区域管理等。通过这些方法，可以方便地在 Unity 中实现复杂的富文本操作，提高用户交互体验。