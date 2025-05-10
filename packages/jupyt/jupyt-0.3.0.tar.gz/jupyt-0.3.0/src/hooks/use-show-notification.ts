export const showNotification = (
  message: string,
  type: 'success' | 'error'
) => {
  const notification = document.createElement('div');
  notification.style.position = 'fixed';
  notification.style.top = '20px';
  notification.style.right = '20px';
  notification.style.backgroundColor =
    type === 'success' ? '#4caf50' : '#f44336';
  notification.style.color = 'white';
  notification.style.padding = '16px';
  notification.style.borderRadius = '4px';
  notification.style.zIndex = '1000';
  notification.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(
    () => {
      document.body.removeChild(notification);
    },
    type === 'success' ? 3000 : 5000
  );
};
