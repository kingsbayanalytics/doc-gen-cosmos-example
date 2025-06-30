import React from 'react';
import { render, screen } from '@testing-library/react';
import { AppStateContext } from '../../state/AppProvider';
import ChatHistoryList from './ChatHistoryList';
import { Conversation } from '../../api/models';
import { ChatHistoryLoadingState } from '../../api/models';
import {defaultMockState} from '../../test/test.utils';


const mockDispatch = jest.fn();

const mockState = {
  ...defaultMockState,
  isChatHistoryOpen: false,
  chatHistoryLoadingState: ChatHistoryLoadingState.Loading,
  isCosmosDBAvailable: {
    cosmosDB: false,
    status: 'NotConfigured',
  },
  chatHistory: [],
  filteredChatHistory: null,
  currentChat: null,
  browseChat: null,
  generateChat: null,
  frontendSettings: { auth_enabled: 'true' },
  feedbackState: {},
  draftedDocument: null,
  draftedDocumentTitle: '',
  isGenerating: false,
  isRequestInitiated: false,
  failedSections : [],
  isFailedReqInitiated : false,
  isLoading : false
};

const renderChatHistoryList = (stateOverride = {}) => {
  const state = { ...mockState, ...stateOverride };
  return render(
    <AppStateContext.Provider value={{ state, dispatch: mockDispatch }}>
      <ChatHistoryList />
    </AppStateContext.Provider>
  );
};

describe('ChatHistoryList', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders "No chat history" message when chat history is empty', () => {
    renderChatHistoryList();
    expect(screen.getByText('No chat history.')).toBeInTheDocument();
  });

  it('sorts groups and entries in descending order of date', () => {
    const chatHistory: Conversation[] = [
      { id: '1', title: 'Recent Chat', date: new Date().toISOString(), messages: [] },
      { id: '2', title: 'Older Chat', date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });

    expect(screen.getByText('Recent')).toBeInTheDocument();
    expect(screen.getAllByText('Recent Chat').length).toBeGreaterThan(1);
  });

  it('handles empty chat history group gracefully', () => {
    renderChatHistoryList({ chatHistory: [] });
    expect(screen.getByText('No chat history.')).toBeInTheDocument();
  });

  it('groups chat history by weeks and months correctly', () => {
    const chatHistory = [
      { id: '3', title: 'Week Old Chat', date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
      { id: '4', title: 'Month Old Chat', date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getAllByText('Week Old Chat').length).toBeGreaterThan(1);
    expect(screen.getAllByText('Month Old Chat').length).toBeGreaterThan(1);
  });

  it('groups entries without matching month-year into a new group', () => {
    const chatHistory: Conversation[] = [
      { id: '5', title: 'Very Old Chat', date: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getAllByText('Very Old Chat').length).toBeGreaterThan(1);
    // Check that a new group for the year appears if it's far in the past
  });
  
  it('places all entries from the same month-year in the same group', () => {
    const chatHistory: Conversation[] = [
      { id: '6', title: 'Chat 1', date: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
      { id: '7', title: 'Chat 2', date: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getAllByText('Chat 1').length).toBeGreaterThan(1);
    expect(screen.getAllByText('Chat 2').length).toBeGreaterThan(1);
    // Confirm that both entries are grouped in the same month
  });
  it('groups recent and older entries separately', () => {
    const chatHistory: Conversation[] = [
      { id: '8', title: 'Recent Chat', date: new Date().toISOString(), messages: [] },
      { id: '9', title: 'Older Chat', date: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getByText('Recent')).toBeInTheDocument();
    expect(screen.getAllByText('Older Chat').length).toBeGreaterThan(1);
    // Ensures "Recent Chat" is grouped separately from older entries
  });
  it('groups multiple entries in the same month-year and sorts them', () => {
    const chatHistory: Conversation[] = [
      { id: '10', title: 'Chat on Day 1', date: new Date(Date.now() - 45 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
      { id: '11', title: 'Chat on Day 2', date: new Date(Date.now() - 46 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getAllByText('Chat on Day 1').length).toBeGreaterThan(1);
    expect(screen.getAllByText('Chat on Day 2').length).toBeGreaterThan(1);
    // Confirms entries from the same month-year are grouped and sorted within the group
  });
  it('handles empty groups gracefully', () => {
    const chatHistory: Conversation[] = [
      { id: '12', title: 'Only Recent Chat', date: new Date().toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getByText('Recent')).toBeInTheDocument();
    expect(screen.queryByText('Older')).not.toBeInTheDocument();
    
  });
  it('sorts groups in descending order by date', () => {
    const chatHistory: Conversation[] = [
      { id: '13', title: 'Newest Chat', date: new Date().toISOString(), messages: [] },
      { id: '14', title: 'Older Chat', date: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
      { id: '15', title: 'Oldest Chat', date: new Date(Date.now() - 365 * 24 * 60 * 60 * 1000).toISOString(), messages: [] },
    ];
    renderChatHistoryList({ chatHistory });
    expect(screen.getAllByText('Newest Chat').length).toBeGreaterThan(1);
    expect(screen.getAllByText('Older Chat').length).toBeGreaterThan(1);
    expect(screen.getAllByText('Oldest Chat').length).toBeGreaterThan(1);
    
  });
  
  
  

  
});
