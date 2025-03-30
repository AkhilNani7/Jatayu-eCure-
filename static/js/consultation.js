// JavaScript for Virtual Consultation functionality

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const localVideo = document.getElementById('local-video');
    const remoteVideo = document.getElementById('remote-video');
    const btnToggleAudio = document.getElementById('btn-toggle-audio');
    const btnToggleVideo = document.getElementById('btn-toggle-video');
    const btnShareScreen = document.getElementById('btn-share-screen');
    const btnEndCall = document.getElementById('btn-end-call');
    const connectionStatus = document.getElementById('connection-status');
    const callTimer = document.getElementById('call-timer');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const saveNotesBtn = document.getElementById('save-notes');
    const consultationNotes = document.getElementById('consultation-notes');
    
    // State variables
    let localStream = null;
    let remoteStream = null;
    let screenShareStream = null;
    let isAudioMuted = false;
    let isVideoOff = false;
    let isScreenSharing = false;
    let callDuration = 0;
    let callTimerInterval = null;
    let peerConnection = null;
    let dataChannel = null;
    
    // Initialize consultation
    async function initConsultation() {
        try {
            // Request user media with audio and video
            localStream = await navigator.mediaDevices.getUserMedia({
                audio: true,
                video: true
            });
            
            // Display local video
            if (localVideo) {
                localVideo.appendChild(document.createElement('video'));
                const videoElement = localVideo.querySelector('video');
                videoElement.srcObject = localStream;
                videoElement.autoplay = true;
                videoElement.muted = true; // Mute local video to prevent feedback
                videoElement.style.width = '100%';
                videoElement.style.height = '100%';
                videoElement.style.objectFit = 'cover';
                videoElement.style.borderRadius = '0.25rem';
                
                // Hide placeholder once video is loaded
                videoElement.onloadedmetadata = () => {
                    const placeholder = document.getElementById('local-video-placeholder');
                    if (placeholder) placeholder.style.display = 'none';
                };
            }
            
            // Simulate connection status (in a real app, this would connect to a signaling server)
            updateConnectionStatus('Connecting...');
            
            // Simulate doctor joining after 3 seconds
            setTimeout(simulateDoctorJoining, 3000);
            
        } catch (error) {
            console.error('Error accessing media devices:', error);
            updateConnectionStatus('Failed to access camera/microphone');
            showErrorMessage('Could not access your camera or microphone. Please make sure they are connected and permissions are granted.');
        }
    }
    
    // Simulate doctor joining the consultation
    function simulateDoctorJoining() {
        // In a real application, this would be handled by a signaling server
        // and WebRTC peer connection setup
        updateConnectionStatus('Connected');
        startCallTimer();
        
        // Simulate remote video (in a real app, this would come from the peer connection)
        if (remoteVideo) {
            // Create a simulated remote video element
            remoteVideo.appendChild(document.createElement('video'));
            const doctorVideo = remoteVideo.querySelector('video');
            doctorVideo.style.width = '100%';
            doctorVideo.style.height = '100%';
            doctorVideo.style.objectFit = 'cover';
            doctorVideo.style.borderRadius = '0.25rem';
            
            // Hide placeholder
            const placeholder = document.getElementById('remote-video-placeholder');
            if (placeholder) placeholder.style.display = 'none';
            
            // In a real application, the remote stream would come from RTCPeerConnection
            // For demo purposes, we'll just show a color
            doctorVideo.poster = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 100 100"><rect width="100%" height="100%" fill="%23212529"/><text x="50%" y="50%" font-family="Arial" font-size="12" text-anchor="middle" fill="%23fff">Doctor\'s Video</text></svg>';
        }
        
        // Add initial system message to chat
        addSystemMessage('Dr. has joined the consultation. You can start chatting now.');
    }
    
    // Toggle audio mute/unmute
    function toggleAudio() {
        if (localStream) {
            const audioTracks = localStream.getAudioTracks();
            if (audioTracks.length > 0) {
                audioTracks[0].enabled = !audioTracks[0].enabled;
                isAudioMuted = !audioTracks[0].enabled;
                
                // Update button UI
                if (btnToggleAudio) {
                    if (isAudioMuted) {
                        btnToggleAudio.innerHTML = '<i class="fas fa-microphone-slash"></i>';
                        btnToggleAudio.classList.replace('btn-outline-info', 'btn-outline-danger');
                    } else {
                        btnToggleAudio.innerHTML = '<i class="fas fa-microphone"></i>';
                        btnToggleAudio.classList.replace('btn-outline-danger', 'btn-outline-info');
                    }
                }
                
                addSystemMessage(isAudioMuted ? 'You muted your microphone.' : 'You unmuted your microphone.');
            }
        }
    }
    
    // Toggle video on/off
    function toggleVideo() {
        if (localStream) {
            const videoTracks = localStream.getVideoTracks();
            if (videoTracks.length > 0) {
                videoTracks[0].enabled = !videoTracks[0].enabled;
                isVideoOff = !videoTracks[0].enabled;
                
                // Update button UI
                if (btnToggleVideo) {
                    if (isVideoOff) {
                        btnToggleVideo.innerHTML = '<i class="fas fa-video-slash"></i>';
                        btnToggleVideo.classList.replace('btn-outline-info', 'btn-outline-danger');
                        
                        // Show placeholder when video is off
                        const placeholder = document.getElementById('local-video-placeholder');
                        if (placeholder) placeholder.style.display = 'block';
                    } else {
                        btnToggleVideo.innerHTML = '<i class="fas fa-video"></i>';
                        btnToggleVideo.classList.replace('btn-outline-danger', 'btn-outline-info');
                        
                        // Hide placeholder when video is on
                        const placeholder = document.getElementById('local-video-placeholder');
                        if (placeholder) placeholder.style.display = 'none';
                    }
                }
                
                addSystemMessage(isVideoOff ? 'You turned off your camera.' : 'You turned on your camera.');
            }
        }
    }
    
    // Toggle screen sharing
    async function toggleScreenSharing() {
        try {
            if (!isScreenSharing) {
                // Start screen sharing
                screenShareStream = await navigator.mediaDevices.getDisplayMedia({
                    video: true
                });
                
                // Replace video track with screen share track
                if (localStream && localVideo) {
                    const videoTrack = screenShareStream.getVideoTracks()[0];
                    const sender = peerConnection ? 
                        peerConnection.getSenders().find(s => s.track.kind === 'video') : null;
                    
                    // In a real app with WebRTC, you would update the sender track
                    // For our demo, just update the local video
                    const videoElement = localVideo.querySelector('video');
                    if (videoElement) {
                        const originalStream = videoElement.srcObject;
                        videoElement.srcObject = screenShareStream;
                        
                        // Listen for screen sharing end
                        videoTrack.onended = () => {
                            videoElement.srcObject = originalStream;
                            isScreenSharing = false;
                            updateScreenShareButton();
                            addSystemMessage('You stopped sharing your screen.');
                        };
                    }
                    
                    isScreenSharing = true;
                    updateScreenShareButton();
                    addSystemMessage('You started sharing your screen.');
                }
            } else {
                // Stop screen sharing
                if (screenShareStream) {
                    screenShareStream.getTracks().forEach(track => track.stop());
                    
                    // Restore video from camera
                    if (localVideo) {
                        const videoElement = localVideo.querySelector('video');
                        if (videoElement) {
                            videoElement.srcObject = localStream;
                        }
                    }
                    
                    screenShareStream = null;
                    isScreenSharing = false;
                    updateScreenShareButton();
                    addSystemMessage('You stopped sharing your screen.');
                }
            }
        } catch (error) {
            console.error('Error toggling screen share:', error);
            showErrorMessage('Failed to share your screen. Please make sure screen sharing is enabled in your browser settings.');
        }
    }
    
    // Update screen share button UI
    function updateScreenShareButton() {
        if (btnShareScreen) {
            if (isScreenSharing) {
                btnShareScreen.innerHTML = '<i class="fas fa-desktop"></i> Stop Sharing';
                btnShareScreen.classList.replace('btn-outline-info', 'btn-outline-danger');
            } else {
                btnShareScreen.innerHTML = '<i class="fas fa-desktop"></i>';
                btnShareScreen.classList.replace('btn-outline-danger', 'btn-outline-info');
            }
        }
    }
    
    // End call
    function endCall() {
        // Stop timer
        if (callTimerInterval) {
            clearInterval(callTimerInterval);
            callTimerInterval = null;
        }
        
        // Stop streams
        if (localStream) {
            localStream.getTracks().forEach(track => track.stop());
            localStream = null;
        }
        
        if (screenShareStream) {
            screenShareStream.getTracks().forEach(track => track.stop());
            screenShareStream = null;
        }
        
        // Update UI
        updateConnectionStatus('Disconnected');
        
        // In a real app, close peer connection
        if (peerConnection) {
            peerConnection.close();
            peerConnection = null;
        }
        
        // Add end call message
        addSystemMessage('The consultation has ended.');
        
        // Disable controls
        if (btnToggleAudio) btnToggleAudio.disabled = true;
        if (btnToggleVideo) btnToggleVideo.disabled = true;
        if (btnShareScreen) btnShareScreen.disabled = true;
        if (btnEndCall) btnEndCall.disabled = true;
        
        // Ask if user wants to return to appointments page
        setTimeout(() => {
            if (confirm('The consultation has ended. Return to appointments?')) {
                window.location.href = '/appointments';
            }
        }, 1000);
    }
    
    // Start call timer
    function startCallTimer() {
        if (callTimerInterval) clearInterval(callTimerInterval);
        
        callDuration = 0;
        updateCallTimer();
        
        callTimerInterval = setInterval(() => {
            callDuration++;
            updateCallTimer();
        }, 1000);
    }
    
    // Update call timer display
    function updateCallTimer() {
        if (callTimer) {
            const minutes = Math.floor(callDuration / 60).toString().padStart(2, '0');
            const seconds = (callDuration % 60).toString().padStart(2, '0');
            callTimer.textContent = `${minutes}:${seconds}`;
        }
    }
    
    // Update connection status display
    function updateConnectionStatus(status) {
        if (connectionStatus) {
            connectionStatus.textContent = status;
            
            // Update badge color based on status
            connectionStatus.className = 'badge';
            switch (status) {
                case 'Connected':
                    connectionStatus.classList.add('bg-success');
                    break;
                case 'Connecting...':
                    connectionStatus.classList.add('bg-warning');
                    break;
                case 'Disconnected':
                    connectionStatus.classList.add('bg-danger');
                    break;
                default:
                    connectionStatus.classList.add('bg-secondary');
            }
        }
    }
    
    // Add message to chat
    function addChatMessage(sender, message, isUser = false) {
        if (chatMessages) {
            // Remove "no messages" placeholder if present
            const placeholder = chatMessages.querySelector('.text-center.text-muted');
            if (placeholder) placeholder.remove();
            
            // Create message element
            const messageEl = document.createElement('div');
            messageEl.className = `chat-message mb-2 ${isUser ? 'text-end' : ''}`;
            
            const senderSpan = document.createElement('span');
            senderSpan.className = `fw-bold ${isUser ? 'text-info' : ''}`;
            senderSpan.textContent = sender + ': ';
            
            const messageText = document.createElement('span');
            messageText.textContent = message;
            
            messageEl.appendChild(senderSpan);
            messageEl.appendChild(messageText);
            
            chatMessages.appendChild(messageEl);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Add system message to chat
    function addSystemMessage(message) {
        if (chatMessages) {
            // Remove "no messages" placeholder if present
            const placeholder = chatMessages.querySelector('.text-center.text-muted');
            if (placeholder) placeholder.remove();
            
            // Create message element
            const messageEl = document.createElement('div');
            messageEl.className = 'chat-message system-message text-center mb-2';
            
            const messageText = document.createElement('small');
            messageText.className = 'text-muted';
            messageText.textContent = message;
            
            messageEl.appendChild(messageText);
            chatMessages.appendChild(messageEl);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Show error message
    function showErrorMessage(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-circle me-2"></i>${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insert after video container
        const videoContainer = document.querySelector('.card-body');
        if (videoContainer) {
            videoContainer.insertBefore(alertDiv, videoContainer.firstChild);
        }
    }
    
    // Save consultation notes
    function saveConsultationNotes() {
        if (consultationNotes) {
            const notes = consultationNotes.value.trim();
            if (notes) {
                // In a real app, this would send notes to the server
                // For demo, just show a success message
                const savedIndicator = document.createElement('div');
                savedIndicator.className = 'alert alert-success mt-2';
                savedIndicator.textContent = 'Notes saved successfully!';
                
                consultationNotes.parentNode.appendChild(savedIndicator);
                
                // Remove indicator after 2 seconds
                setTimeout(() => {
                    savedIndicator.remove();
                }, 2000);
            }
        }
    }
    
    // Event Listeners
    if (btnToggleAudio) {
        btnToggleAudio.addEventListener('click', toggleAudio);
    }
    
    if (btnToggleVideo) {
        btnToggleVideo.addEventListener('click', toggleVideo);
    }
    
    if (btnShareScreen) {
        btnShareScreen.addEventListener('click', toggleScreenSharing);
    }
    
    if (btnEndCall) {
        btnEndCall.addEventListener('click', endCall);
    }
    
    if (chatForm && chatInput) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (message) {
                // Add user message to chat
                addChatMessage('You', message, true);
                chatInput.value = '';
                
                // Simulate doctor response after 1-2 seconds
                setTimeout(() => {
                    // In a real app, this would be sent via WebRTC data channel or websockets
                    addChatMessage('Dr.', 'I see. Could you please provide more details about your symptoms?');
                }, 1000 + Math.random() * 1000);
            }
        });
    }
    
    if (saveNotesBtn) {
        saveNotesBtn.addEventListener('click', saveConsultationNotes);
    }
    
    // Initialize the consultation when page loads
    initConsultation();
});
